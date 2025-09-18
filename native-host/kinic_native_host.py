#!/usr/bin/env python3
"""
Kinic Native Host (Python)

Implements Chrome Native Messaging host with:
- Stdin/stdout JSON framing per Chrome spec (32-bit native-endian length prefix)
- Local HTTP API to trigger Kinic extension actions via the open native port

Day-1 scope (per requirements):
- Action: kinic.store (saving the active tab by default, or a provided URL)
- HTTP endpoints: /api/status (GET), /api/kinic/store (POST)
- Response schema bridging: native {id, ok, result|error} -> HTTP {success, message, data}

Notes:
- All logs are emitted to stderr to avoid corrupting stdout protocol.
- On Windows, switches stdin/stdout to binary mode.
- The process lifetime is tied to the native port; when Chrome disconnects,
  stdin closes and we terminate.
"""

from __future__ import annotations

import sys
import os
import json
import struct
import threading
import uuid
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

# HTTP server (lightweight Flask)
try:
    from flask import Flask, request, jsonify
except Exception as e:  # pragma: no cover
    print("Flask is required: pip install flask", file=sys.stderr)
    raise


# ----- Platform-specific stdio binary mode (Windows) -----
if os.name == "nt":  # Windows
    try:
        import msvcrt  # type: ignore

        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    except Exception as e:  # pragma: no cover
        print(f"Failed to set binary mode on Windows: {e}", file=sys.stderr)


# ----- Native messaging codec -----
class NativeCodec:
    """Read/write Chrome Native Messaging frames to stdin/stdout."""

    def __init__(self):
        self._out_lock = threading.Lock()

    @staticmethod
    def _read_exact(stream, n: int) -> bytes:
        buf = b""
        while len(buf) < n:
            chunk = stream.read(n - len(buf))
            if not chunk:
                return b""
            buf += chunk
        return buf

    def read_message(self) -> Optional[Dict[str, Any]]:
        header = self._read_exact(sys.stdin.buffer, 4)
        if len(header) != 4:
            return None  # EOF or broken pipe
        (length,) = struct.unpack("I", header)  # native-endian uint32
        if length == 0:
            return {}
        body = self._read_exact(sys.stdin.buffer, length)
        if len(body) != length:
            return None
        try:
            return json.loads(body.decode("utf-8"))
        except Exception as e:  # pragma: no cover
            print(f"Failed to decode JSON from extension: {e}", file=sys.stderr)
            return None

    def write_message(self, msg: Dict[str, Any]) -> None:
        data = json.dumps(msg, ensure_ascii=False).encode("utf-8")
        header = struct.pack("I", len(data))
        with self._out_lock:
            sys.stdout.buffer.write(header)
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()


# ----- Correlated request/response handling -----
@dataclass
class Pending:
    event: threading.Event
    response: Optional[Dict[str, Any]] = None


class NativePort:
    """Manages correlated messages over the native messaging channel."""

    def __init__(self) -> None:
        self.codec = NativeCodec()
        self.pending: Dict[str, Pending] = {}
        self.connected = True  # Host is launched by Chrome; connected unless EOF
        self.origin: Optional[str] = None
        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._lock = threading.Lock()
        self._last_rx: Optional[float] = None
        self._started_at = time.time()

    def start(self, origin: Optional[str]) -> None:
        self.origin = origin
        self._reader_thread.start()

    def _reader_loop(self) -> None:
        while True:
            msg = self.codec.read_message()
            if msg is None:
                print("Native port closed by Chrome (EOF)", file=sys.stderr)
                self.connected = False
                # Give the HTTP server some time to respond 503 before exiting
                time.sleep(0.2)
                os._exit(0)  # terminate host; Chrome will relaunch on reconnect
            self._last_rx = time.time()

            # Extension may send responses or unsolicited events
            msg_id = msg.get("id")
            if msg_id and msg_id in self.pending:
                p = self.pending.pop(msg_id, None)
                if p:
                    p.response = msg
                    p.event.set()
            else:
                # Unsolicited message; log to stderr
                print(f"Unsolicited from extension: {msg}", file=sys.stderr)

    def request(self, action: str, params: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        if not self.connected:
            raise RuntimeError("native_port_disconnected")
        req_id = str(uuid.uuid4())
        payload = {"id": req_id, "action": action, "params": params or {}}
        pending = Pending(event=threading.Event())
        with self._lock:
            self.pending[req_id] = pending
            # Write outside the lock for safety
        self.codec.write_message(payload)

        ok = pending.event.wait(timeout)
        if not ok:
            # cleanup
            with self._lock:
                self.pending.pop(req_id, None)
            raise TimeoutError("native_request_timeout")
        assert pending.response is not None
        return pending.response

    def status(self) -> Dict[str, Any]:
        return {
            "connected": self.connected,
            "origin": self.origin,
            "pending": len(self.pending),
            "last_message_at": self._last_rx,
            "uptime_sec": round(time.time() - self._started_at, 1),
        }


# ----- HTTP API -----
app = Flask(__name__)
native_port = NativePort()


@app.route("/api/status", methods=["GET"])
def api_status():
    s = native_port.status()
    http = {"success": True, "message": "ok", "data": s}
    if not s["connected"]:
        return jsonify({"success": False, "message": "extension_disconnected", "data": s}), 503
    return jsonify(http)


@app.route("/api/kinic/store", methods=["POST"])
def api_kinic_store():
    if not native_port.connected:
        return jsonify({"success": False, "message": "extension_disconnected"}), 503

    try:
        body = request.get_json(silent=True) or {}
        # Allowed fields per spec
        allowed = {"url", "title", "tags", "notes", "content", "selection", "metadata"}
        params = {k: v for k, v in body.items() if k in allowed}

        # If no URL provided, extension should save active tab
        resp = native_port.request("kinic.store", params, timeout=float(os.getenv("KINIC_STORE_TIMEOUT", 30)))

        ok = bool(resp.get("ok"))
        if ok:
            return jsonify({"success": True, "message": "stored", "data": resp.get("result")})
        else:
            return jsonify({"success": False, "message": str(resp.get("error") or "error"), "data": None}), 500

    except TimeoutError:
        return jsonify({"success": False, "message": "timeout"}), 504
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/kinic/retrieve", methods=["POST"])
def api_kinic_retrieve():
    """Minimal retrieval API -> native 'kinic.retrieve' action.

    Accepts: { query: string, top_k?: number, filters?: object }
    """
    if not native_port.connected:
        return jsonify({"success": False, "message": "extension_disconnected"}), 503

    try:
        body = request.get_json(silent=True) or {}
        query = body.get("query", "")
        if not isinstance(query, str) or not query.strip():
            return jsonify({"success": False, "message": "query_required"}), 400

        params: Dict[str, Any] = {
            "query": query.strip(),
        }
        top_k = body.get("top_k")
        if isinstance(top_k, int) and 1 <= top_k <= 100:
            params["top_k"] = top_k
        filters = body.get("filters")
        if isinstance(filters, dict):
            params["filters"] = filters

        resp = native_port.request("kinic.retrieve", params, timeout=float(os.getenv("KINIC_RETRIEVE_TIMEOUT", 30)))
        ok = bool(resp.get("ok"))
        if ok:
            return jsonify({"success": True, "message": "ok", "data": resp.get("result")})
        else:
            return jsonify({"success": False, "message": str(resp.get("error") or "error"), "data": None}), 500
    except TimeoutError:
        return jsonify({"success": False, "message": "timeout"}), 504
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def main():
    # Chrome provides origin as argv[1] (e.g., chrome-extension://<ID>/)
    origin = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"Kinic Native Host starting. Origin={origin}", file=sys.stderr)

    # Start native reader thread
    native_port.start(origin)

    # Start HTTP server; unauthenticated localhost per requirements
    host = os.getenv("KINIC_HOST", "127.0.0.1")
    port = int(os.getenv("KINIC_PORT", "5007"))
    debug = os.getenv("KINIC_DEBUG", "false").lower() == "true"
    print(f"HTTP API on http://{host}:{port}", file=sys.stderr)

    # Threaded=True to allow concurrent requests while waiting for native replies
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    main()
