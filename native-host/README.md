# Kinic Native Host (Chrome Native Messaging)

This is a Python native host that lets your local app trigger actions in the Kinic Chrome extension via Chrome Native Messaging. It exposes a tiny HTTP API so any local process can save websites programmatically.

## What’s included
- `kinic_native_host.py`: Native host with stdin/stdout framing and an HTTP API
- `manifest/`: Host manifest templates for macOS and Windows
- `install_macos.sh`, `install_windows.ps1`: Install helpers (user scope)
- `uninstall_macos.sh`, `uninstall_windows.ps1`: Removal helpers
- `requirements.txt`: Python dependencies
- `smoke_test.sh`: Quick HTTP smoke test
- `examples/`: Service worker and content script examples

## Actions (Day 1)
- `kinic.store`: Save the active tab by default, or a provided URL
  - Accepted fields: `url`, `title`, `tags`, `notes`, `content`, `selection`, `metadata`
  - The extension should emit a definitive “stored” response; the host waits and returns it
 - `kinic.retrieve`: Minimal retrieval by query
   - Accepted fields: `query` (required), `top_k` (optional), `filters` (optional)

## HTTP API
- `GET /api/status` → `{ success, message, data: { connected, origin, pending, last_message_at, uptime_sec } }`
- `POST /api/kinic/store` (JSON body with fields above)
  - Response on success: `{ success: true, message: "stored", data: { /* extension result */ } }`
  - Response on error: `{ success: false, message: "..." }`
 - `POST /api/kinic/retrieve` (JSON: `{ query, top_k?, filters? }`)
   - Response on success: `{ success: true, message: "ok", data: { /* extension result */ } }`
   - Response on error: `{ success: false, message: "..." }`

## Install (macOS)
1) Ensure Python 3 and Flask are available, then:

```
cd native-host
python3 -m pip install -r requirements.txt
./install_macos.sh
```

This writes the manifest to:
`~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.kinic.api.json` and points it at `kinic_native_host.py`.

Edit the manifest to replace `DEV_EXTENSION_ID` and `PROD_EXTENSION_ID` with your IDs.

Uninstall:

```
./uninstall_macos.sh
```

## Install (Windows)
1) Ensure Python 3 is installed and available via `py` launcher, then:

```
cd native-host
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\install_windows.ps1
```

This creates a manifest in `%LocalAppData%\Kinic\NativeMessagingHosts\com.kinic.api.json`, points it to `kinic_native_host.bat`, and sets the registry key:
`HKCU\Software\Google\Chrome\NativeMessagingHosts\com.kinic.api`

Edit the manifest to replace `DEV_EXTENSION_ID` and `PROD_EXTENSION_ID` with your IDs.

Uninstall:

```
powershell -ExecutionPolicy Bypass -File .\uninstall_windows.ps1
```

## Extension examples (service worker + content script)
Make sure your MV3 extension adds the nativeMessaging permission and keeps a persistent port open. Include a content script if you prefer message-based capture, or use `chrome.scripting.executeScript` from the service worker.

```
// manifest.json
{
  "manifest_version": 3,
  "name": "Kinic",
  "version": "0.0.0",
  "background": { "service_worker": "sw.js" },
  "permissions": ["nativeMessaging"]
}
```

```
See examples:
- Service worker: `native-host/examples/sw_example.js`
- Content script: `native-host/examples/content_script.js`

Quick installable example: `native-host/example-extension.zip`
- Load unpacked (or unzip and load folder) at chrome://extensions
- After install, note the extension ID and rerun installer with IDs to update host manifest, e.g.:
  - macOS:
    - `DEV_ID=<your_id> PROD_ID=<your_id> ./install_macos.sh`
  - Windows:
    - `powershell -ExecutionPolicy Bypass -File .\install_windows.ps1 -DevId <your_id> -ProdId <your_id>`

## Smoke test
With the extension installed and the service worker connected (native host process should be running):

```
# From repo root
cd native-host
./smoke_test.sh
```

You should see status JSON and a `kinic.store` call result.

## Plain-English Overview
- The native host is a tiny local program Chrome launches on demand. The extension connects to it over a pipe (stdin/stdout) and both sides exchange JSON messages framed by a 32-bit length prefix.
- Your local apps can call a simple HTTP API on `http://127.0.0.1:5007`. The host forwards requests to the extension via the open native port.
- The extension does the real work (saving pages, retrieving memories) and replies; the host bridges that back to HTTP.

## Examples
- Save current tab:

```
curl -s -X POST http://127.0.0.1:5007/api/kinic/store -H 'Content-Type: application/json' -d '{}'
```

- Save specific URL with tags/notes:

```
curl -s -X POST http://127.0.0.1:5007/api/kinic/store \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://kinic.io","tags":["docs","kinic"],"notes":"homepage"}'
```

- Retrieve by query:

```
curl -s -X POST http://127.0.0.1:5007/api/kinic/retrieve \
  -H 'Content-Type: application/json' \
  -d '{"query":"auth tokens","top_k":3}'
```

- Python snippet:

```
import requests

base = 'http://127.0.0.1:5007'

# Store
resp = requests.post(f'{base}/api/kinic/store', json={"url": "https://kinic.io", "tags": ["docs"]})
print(resp.json())

# Retrieve
resp = requests.post(f'{base}/api/kinic/retrieve', json={"query": "kinic docs", "top_k": 5})
print(resp.json())
```

## Troubleshooting Tips
- “host not found”: Manifest not in the right place or `allowed_origins` missing your extension ID.
- HTTP 503 `extension_disconnected`: Service worker not connected. Ensure `connectNative()` runs on startup and stays connected.
- Large pages: If content is huge, prefer saving just `url`, and let your backend fetch/ingest content. Message limit host→extension is 1 MB.

## Notes
- The native host only prints JSON frames to stdout. All logs go to stderr.
- The host exits when Chrome closes stdin (e.g., on disconnect). The service worker should reconnect and Chrome will relaunch the host.
- Message size: host→extension is limited to 1 MB. The `kinic.store` payloads are typically small; for larger data, prefer passing a URL or minimal metadata.

## Troubleshooting
- “Specified native messaging host not found”: manifest not installed or `allowed_origins`/`path` incorrect.
- HTTP 503 `extension_disconnected`: ensure the extension’s service worker is running and connected.
- Windows: if Python isn’t on `py` launcher, edit `kinic_native_host.bat` accordingly.
