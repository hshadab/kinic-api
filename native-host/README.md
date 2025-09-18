# Kinic Native Host (Chrome Native Messaging)

This is a Python native host that lets your local app trigger actions in the Kinic Chrome extension via Chrome Native Messaging. It exposes a tiny HTTP API so any local process can save websites programmatically.

## Plain-English Background & Quick Overview
- Adds a tiny local “bridge” that Chrome launches on demand. Your extension keeps a persistent connection to it, and the bridge exposes a simple local HTTP API.
- Any desktop app can now ask the extension to store the active tab (or a URL) and retrieve results—without fragile UI automation.
- How it works at a glance:
  - The extension opens a native port to `com.kinic.api` and listens for `{ id, action, params }`.
  - The native host exposes `http://127.0.0.1:5007/api/kinic/*`, forwards requests to the extension, then returns `{ success, message, data }`.
  - Keep messages small; the extension does the heavy lifting (page capture, persistence, search).

### Step-by-Step Example
1) Load the example extension
   - `chrome://extensions` → Developer Mode → Load unpacked → select `native-host/example-extension` (or unzip `example-extension.zip`)
   - Copy the extension ID (32 characters)
2) Install the native host manifest with your extension ID
   - macOS: `cd native-host && DEV_ID=<your_id> PROD_ID=<your_id> ./install_macos.sh`
   - Windows (PowerShell): `cd native-host && powershell -ExecutionPolicy Bypass -File .\\install_windows.ps1 -DevId <your_id> -ProdId <your_id>`
3) Open a web page in Chrome (e.g., https://kinic.io) so there’s an active tab
4) Save the active tab
   - `curl -s -X POST http://127.0.0.1:5007/api/kinic/store -H 'Content-Type: application/json' -d '{}'`
   - Expect `{ "success": true, "message": "stored", "data": { ... } }`
5) Retrieve results
   - `curl -s -X POST http://127.0.0.1:5007/api/kinic/retrieve -H 'Content-Type: application/json' -d '{"query":"test"}'`
   - Expect `{ "success": true, "data": { "items": [...] } }`
6) Replace stubs in the example service worker with your real Kinic save/retrieve code.

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

## Troubleshooting Tips
- “host not found”: Manifest not in the right place or `allowed_origins` missing your extension ID.
- HTTP 503 `extension_disconnected`: Service worker not connected. Ensure `connectNative()` runs on startup and stays connected.
- Large pages: If content is huge, prefer saving just `url`, and let your backend fetch/ingest content. Message limit host→extension is 1 MB.

## Background & Architecture

This setup splits responsibilities cleanly between three parties:

- Extension (MV3 service worker)
  - Knows the browser, tabs, and page content
  - Implements the real Kinic logic (store/retrieve, auth to your backend, etc.)
  - Keeps a persistent native port to the local host open

- Native host (this folder)
  - A small local process Chrome launches when the extension calls `connectNative()`
  - Speaks Chrome’s native messaging protocol (stdin/stdout with 32‑bit length prefix)
  - Exposes a local HTTP API so any local app (CLI, UI, other services) can trigger Kinic actions
  - Correlates requests with `{ id }` and bridges extension responses back to HTTP

- Your local apps
  - Call `http://127.0.0.1:5007/api/kinic/store` and `/api/kinic/retrieve`
  - Don’t need to know about Chrome’s native messaging details

### Architecture Diagram

```
┌─────────────┐   HTTP (localhost)    ┌─────────────────────────────┐
│  Local App  │  ───────────────────▶ │   Native Host (this repo)   │
│ (CLI/UI/etc)│   /api/kinic/*        │  - HTTP server (5007)       │
└─────────────┘                        │  - Native messaging bridge  │
                                       └─────────────┬──────────────┘
                                                     │ stdio (framed JSON)
                                                     ▼
                                         ┌───────────────────────────┐
                                         │ Chrome Extension (MV3 SW) │
                                         │ - connectNative(HOST)     │
                                         │ - kinic.store/retrieve    │
                                         │ - tabs/scripting/content  │
                                         └─────────────┬─────────────┘
                                                       │
                                                       ▼
                                             ┌──────────────────┐
                                             │  Web Page / Tab  │
                                             └──────────────────┘
```

### Why a persistent port?

- `chrome.runtime.connectNative(HOST)` creates one long‑lived process/pipe, keeping the MV3 service worker alive and allowing the host to accept triggers at any time.
- `chrome.runtime.sendNativeMessage()` would spawn a new host process per call and not keep the worker alive; that makes push‑style flows and low‑latency repeated calls harder.

### Message Contract (boring and explicit)

- Host → Extension
  - `{ "id": "uuid", "action": "kinic.store", "params": { /* small */ } }`
  - `{ "id": "uuid", "action": "kinic.retrieve", "params": { "query": "...", "top_k?": N } }`

- Extension → Host
  - `{ "id": "uuid", "ok": true,  "result": { /* result */ } }`
  - `{ "id": "uuid", "ok": false, "error": "..." }`

The native host correlates by `id` and returns stable HTTP shapes:

- `{ success: true/false, message: string, data?: any }`

### MV3 Lifecycle Considerations

- A native port connection prevents the service worker from going idle. If the host exits, the port closes and the worker can stop; the SW should reconnect in `onDisconnect`.
- Keep payloads small. Pass URLs or minimal metadata; let the extension/backend fetch heavy content.
- Use `tabs` and `scripting` permissions to access page context. You may use `activeTab` as a more restrictive alternative.

### Security & Size Limits

- Native messaging host manifests must list your extension IDs in `allowed_origins`.
- Host path must be absolute (macOS/Linux). Windows requires a registry key pointing to the manifest path.
- Size limits (Chrome): host→extension ~1 MB; extension→host ~64 MB. Design responses to fit comfortably below these.
- This HTTP bridge is local and unauthenticated by design (per requirements). If needed, add a token header or bind only to `127.0.0.1` (already default).

### Installation Paths (User Scope)

- macOS: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.kinic.api.json`
- Linux: `~/.config/google-chrome/NativeMessagingHosts/com.kinic.api.json` (template not included here; similar to macOS)
- Windows: Manifest anywhere + registry key at `HKCU\Software\Google\Chrome\NativeMessagingHosts\com.kinic.api`

### Typical Flows

- Store active tab
  - Local app → HTTP `POST /api/kinic/store {}`
  - Host → Extension `kinic.store` without `url`
  - Extension determines active tab, optionally captures selection/content, performs save, and replies with result

- Store arbitrary URL
  - Local app → HTTP `POST /api/kinic/store { url, tags, notes }`
  - Extension loads/extracts (if needed) or simply records metadata and URL, and replies with a definitive success

- Retrieve
  - Local app → HTTP `POST /api/kinic/retrieve { query, top_k }`
  - Extension runs its search against Kinic memory and returns small summaries

### Why this vs. UI automation

- Previous flows in this repo used pyautogui to drive the UI. Native messaging avoids coordinate fragility, timing issues, and OS differences.
- With native messaging, the extension remains the canonical source of truth for browsing context and Kinic operations, while the host provides a clean local API for apps.

### Integration Checklist

- [ ] Add `nativeMessaging`, `tabs`, and `scripting` permissions in `manifest.json`
- [ ] Implement a service worker that:
  - [ ] Connects to `com.kinic.api` on install/startup
  - [ ] Handles `kinic.store` and `kinic.retrieve`
  - [ ] Replies with `{ id, ok, result|error }`
- [ ] (Optional) Add a content script for capture, or use `chrome.scripting.executeScript`
- [ ] Install the native host manifest with your extension IDs in `allowed_origins`
- [ ] Run the smoke test and verify both store and retrieve

## Next Steps

1) Install the example extension (or your own) and confirm it connects
- Load `native-host/example-extension` at `chrome://extensions` (Developer Mode → Load unpacked)
- Note the extension ID (a 32‑char string)

2) Install the native host manifest with your extension ID(s)
- macOS:
  - `cd native-host && python3 -m pip install -r requirements.txt`
  - `DEV_ID=<ext_id> PROD_ID=<ext_id> ./install_macos.sh`
- Windows (PowerShell):
  - `cd native-host && pip install -r requirements.txt`
  - `powershell -ExecutionPolicy Bypass -File .\\install_windows.ps1 -DevId <ext_id> -ProdId <ext_id>`

3) Verify connectivity
- `curl -s http://127.0.0.1:5007/api/status` → expect `{ success: true, ... connected: true }`

4) Exercise the API
- `./native-host/smoke_test.sh` (runs store then retrieve)
- Or manual:
  - `curl -s -X POST http://127.0.0.1:5007/api/kinic/store -H 'Content-Type: application/json' -d '{}'`
  - `curl -s -X POST http://127.0.0.1:5007/api/kinic/retrieve -H 'Content-Type: application/json' -d '{"query":"test"}'`

5) Replace stubs with real Kinic logic
- In the service worker, implement actual persistence for `kinic.store` and searching for `kinic.retrieve`
- Keep responses small; return IDs/summaries, not entire documents

6) Productionize (optional)
- Add logging and error reporting in the extension
- Consider per‑user auth tokens for the local HTTP API if needed
- Package installers for multiple Chromium channels (Chrome, Edge, Beta/Canary)


## Notes
- The native host only prints JSON frames to stdout. All logs go to stderr.
- The host exits when Chrome closes stdin (e.g., on disconnect). The service worker should reconnect and Chrome will relaunch the host.
- Message size: host→extension is limited to 1 MB. The `kinic.store` payloads are typically small; for larger data, prefer passing a URL or minimal metadata.

## Troubleshooting
- “Specified native messaging host not found”: manifest not installed or `allowed_origins`/`path` incorrect.
- HTTP 503 `extension_disconnected`: ensure the extension’s service worker is running and connected.
- Windows: if Python isn’t on `py` launcher, edit `kinic_native_host.bat` accordingly.
