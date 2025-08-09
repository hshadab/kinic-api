# Kinic API v5 - Complete Documentation

## Overview

This documentation covers the complete Kinic Desktop Automation API (v5) that we built and configured. The API provides programmatic control over the Kinic Chrome extension through RESTful endpoints, enabling automation of saving pages, searching, retrieving URLs, and extracting AI-generated analysis.

## System Architecture

The API uses a combination of technologies to achieve cross-platform automation:
- **WSL (Windows Subsystem for Linux)** for the Python environment
- **Windows PowerShell** for native mouse/keyboard control
- **Flask** for the REST API server
- **Windows API calls** via PowerShell for precise clicking and text selection

## Installation & Setup

### Prerequisites
- Windows 10/11 with WSL installed
- Chrome browser with Kinic extension
- Python 3.8+ in WSL
- Screen resolution aware setup (coordinates are screen-specific)

### Installation Steps

1. **Navigate to the project directory:**
```bash
cd ~/kinic
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install flask flask-cors pyautogui pyperclip requests
```

## Configuration

The API requires exact screen coordinates for two UI elements:

### 1. Kinic Extension Button Position
The location of the Kinic icon in Chrome's toolbar.

### 2. AI Response Text Area Position  
The location where AI-generated text appears in Kinic.

### Capturing Coordinates

We created multiple tools for capturing coordinates:

#### Quick Capture (10-second timer):
```bash
cd ~/kinic && python3 capture-position-10s.py
```
Position your mouse on the target within 10 seconds.

#### Instant Capture:
```bash
cd ~/kinic && python3 get-position-now.py
```
Position mouse first, then run command.

#### AI Position Capture (Automated):
```bash
cd ~/kinic && python3 capture-ai-position.py
```
This automatically opens Kinic, searches, and waits for you to position the mouse on the AI response.

### Configuration Storage

Coordinates are stored in `~/.kinic/config.json`:
```json
{
  "kinic_x": 1387,
  "kinic_y": 99,
  "ai_response_x": 948,
  "ai_response_y": 830
}
```

## Running the API Server

### Start the server:
```bash
cd ~/kinic
source venv/bin/activate
python kinic-api-v5.py
```

The server runs on `http://localhost:5005`

### Server Output:
```
🚀 Kinic API v5 - Complete with AI Text Extraction
============================================================
Configuration:
  Kinic button: (1387, 99)
  AI response: (948, 830)

Running on http://localhost:5005
```

## API Endpoints

### 1. Click Kinic Button
**Endpoint:** `POST /click`

Opens the Kinic extension popup.

```bash
curl -X POST http://localhost:5005/click
```

**Response:**
```json
{
  "success": true,
  "message": "Clicked at (1387, 99)"
}
```

### 2. Save Current Page
**Endpoint:** `POST /save`

Saves the currently active webpage to Kinic.

```bash
curl -X POST http://localhost:5005/save
```

**Response:**
```json
{
  "success": true,
  "message": "Page saved"
}
```

### 3. Search
**Endpoint:** `POST /search`

Searches your Kinic collection.

```bash
curl -X POST http://localhost:5005/search \
  -H "Content-Type: application/json" \
  -d '{"query":"python tutorial"}'
```

**Response:**
```json
{
  "success": true,
  "message": "Searched: python tutorial"
}
```

### 4. Search and Retrieve URL
**Endpoint:** `POST /search-and-retrieve`

Searches and returns the URL of the first result using the exact sequence:
1. Open Kinic
2. Tab 4 times to search field
3. Enter search term
4. Press Enter
5. Wait 3 seconds
6. Tab 2 times to first result
7. Shift+F10 for context menu
8. Down arrow 5 times
9. Enter to copy URL
10. Extract from clipboard

```bash
curl -X POST http://localhost:5005/search-and-retrieve \
  -H "Content-Type: application/json" \
  -d '{"query":"privacy"}'
```

**Response:**
```json
{
  "success": true,
  "query": "privacy",
  "url": "https://huggingface.co/remzicam/privacy_intent",
  "message": "Retrieved first URL for: privacy"
}
```

### 5. Search and Extract AI Analysis
**Endpoint:** `POST /search-ai-extract`

Searches, triggers AI analysis, and extracts the generated text using triple-click selection.

```bash
curl -X POST http://localhost:5005/search-ai-extract \
  -H "Content-Type: application/json" \
  -d '{"query":"legal"}'
```

**Response:**
```json
{
  "success": true,
  "query": "legal",
  "ai_response": "The \"remzicam/privacy_intent\" repository on Hugging Face appears to be focused on privacy intent...",
  "message": "AI response extracted for: legal"
}
```

### 6. Close Kinic
**Endpoint:** `POST /close`

Closes the Kinic extension popup.

```bash
curl -X POST http://localhost:5005/close
```

### 7. Setup Kinic Position
**Endpoint:** `POST /setup-kinic`

Updates the Kinic button coordinates.

```bash
curl -X POST http://localhost:5005/setup-kinic \
  -H "Content-Type: application/json" \
  -d '{"x":1387,"y":99}'
```

### 8. Setup AI Response Position
**Endpoint:** `POST /setup-ai`

Updates the AI response text area coordinates.

```bash
curl -X POST http://localhost:5005/setup-ai \
  -H "Content-Type: application/json" \
  -d '{"x":948,"y":830}'
```

## Implementation Details

### Mouse Control Method

The API uses Windows PowerShell to control the mouse through Windows API calls:

```python
def windows_click(x, y):
    ps_script = f"""
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern bool SetCursorPos(int X, int Y);
            
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);
            
            public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
            public const uint MOUSEEVENTF_LEFTUP = 0x0004;
        }}
'@
    [Win32]::SetCursorPos({x}, {y})
    Start-Sleep -Milliseconds 100
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 50
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    """
```

### Text Selection Method

For AI text extraction, we use triple-click to select all text:

```python
# Triple-click to select all text
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.2)
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.2)
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.5)

# Copy to clipboard
send_keys("^c")
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Kinic button not clicking correctly
- **Solution:** Recapture coordinates using `capture-position-10s.py`
- Ensure Chrome is maximized and Kinic icon is visible

#### 2. AI text not capturing
- **Issue:** Empty or wrong text captured
- **Solution:** 
  - Recapture AI response position
  - Increase wait time for AI generation (default is 8 seconds)
  - Ensure the AI response is fully loaded before capture

#### 3. WSL mouse control issues
- **Symptoms:** Mouse position stuck at same coordinates
- **Explanation:** WSL can send mouse commands but cannot read Windows mouse position
- **Solution:** Use PowerShell-based position capture tools

#### 4. Near-miss clicks
- **Issue:** Clicks landing slightly off target
- **Solution:** The API v3+ includes near-miss correction that clicks in a small cross pattern

## File Structure

```
~/kinic/
├── kinic-api-v5.py              # Main API server (latest)
├── kinic-api-v4.py              # Previous version with search-retrieve
├── kinic-api-v3.py              # Version with near-miss correction
├── kinic-api-windows.py         # Windows-native clicking version
├── capture-position-10s.py      # 10-second countdown position capture
├── capture-ai-position.py       # Automated AI position capture
├── get-position-now.py          # Instant position capture
├── test-ai-triple-click.py     # Test AI extraction
├── search-and-retrieve.py      # Standalone search tool
├── test-mouse.py                # Mouse control test
├── ~/.kinic/config.json         # Saved coordinates
└── venv/                        # Python virtual environment
```

## Advanced Usage Examples

### Batch Save URLs
```bash
#!/bin/bash
# save-urls.sh
urls=(
  "https://github.com/hshadab/verifiable-agentkit"
  "https://www.rottentomatoes.com/"
  "https://x.com/home"
)

for url in "${urls[@]}"; do
  # Open URL in Chrome
  powershell.exe -Command "Start-Process chrome.exe -ArgumentList '$url'"
  sleep 4
  # Save to Kinic
  curl -X POST http://localhost:5005/save
  sleep 2
done
```

### Extract AI Analysis for Multiple Queries
```python
import requests
import json

queries = ["legal", "privacy", "technology", "AI ethics"]
results = {}

for query in queries:
    response = requests.post(
        'http://localhost:5005/search-ai-extract',
        json={'query': query}
    )
    data = response.json()
    if data['success']:
        results[query] = data['ai_response']

# Save results
with open('ai_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Integration with n8n Workflow
```javascript
// n8n HTTP Request node configuration
{
  "method": "POST",
  "url": "http://localhost:5005/search-ai-extract",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "query": "{{$node.previous.data.searchTerm}}"
  }
}
```

## Performance Considerations

- **Wait times:** Adjust based on your system speed
  - Page load: 3-4 seconds
  - Kinic open: 2 seconds
  - AI response: 8-12 seconds
  
- **Coordinate accuracy:** Coordinates are screen-specific and change with:
  - Screen resolution changes
  - Browser zoom level
  - Toolbar modifications

## Security Notes

- The API runs locally on localhost only
- No authentication by default (add if exposing externally)
- Clipboard operations may expose sensitive data
- PowerShell execution requires appropriate permissions

## Version History

- **v5**: Added AI text extraction with triple-click
- **v4**: Implemented search-and-retrieve with context menu
- **v3**: Added near-miss click correction
- **v2**: Windows-native PowerShell clicking
- **v1**: Initial PyAutoGUI implementation

## Contributing

To add new functionality:

1. Add endpoint to `kinic-api-v5.py`
2. Implement automation sequence
3. Test with standalone script first
4. Update documentation

## Support

For issues related to:
- **Coordinate capture:** Check display settings and browser zoom
- **API errors:** Check Flask logs and Windows Event Viewer
- **Mouse control:** Verify PowerShell execution policy

---

*Built and tested on Windows 11 with WSL2 Ubuntu, Chrome 120+, and Kinic extension v1.0+*