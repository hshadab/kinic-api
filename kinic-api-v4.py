#!/usr/bin/env python3
"""Kinic API v4 - With correct search and retrieve functionality"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    config = {'kinic_x': 959, 'kinic_y': 98}

def save_config():
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def windows_click(x, y):
    """Click at exact position"""
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
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def send_keys(keys):
    """Send keyboard keys"""
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def send_shift_f10():
    """Send Shift+F10 for context menu"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("+{F10}")
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def get_clipboard():
    """Get clipboard content"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    return result.stdout.strip() if result.stdout else None

def focus_chrome():
    """Focus Chrome window"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            [DllImport("user32.dll")]
            public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        }
'@
    $chrome = [Win32]::FindWindow("Chrome_WidgetWin_1", $null)
    if ($chrome -ne [IntPtr]::Zero) {
        [Win32]::SetForegroundWindow($chrome)
    }
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'config': config,
        'endpoints': {
            'POST /click': 'Click Kinic button',
            'POST /save': 'Save current page',
            'POST /search': 'Search - Body: {"query": "text"}',
            'POST /search-and-retrieve': 'Search and get first URL - Body: {"query": "text"}',
            'POST /close': 'Close Kinic',
            'POST /setup': 'Set position - Body: {"x": 959, "y": 98}'
        }
    })

@app.route('/click', methods=['POST'])
def click_kinic():
    """Click Kinic button"""
    try:
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        return jsonify({'success': True, 'message': f"Clicked at ({config['kinic_x']}, {config['kinic_y']})"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
    """Save current page"""
    try:
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        send_keys("+{TAB}")
        time.sleep(0.5)
        send_keys("{ENTER}")
        return jsonify({'success': True, 'message': 'Page saved'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    """Basic search"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query'}), 400
        
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Tab 4 times to search
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.2)
        
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(0.5)
        send_keys("{ENTER}")
        
        return jsonify({'success': True, 'message': f'Searched: {query}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-and-retrieve', methods=['POST'])
def search_and_retrieve():
    """Search and retrieve first URL using correct sequence"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Step 1: Open Kinic
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Step 2: Tab 4 times to search field
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.2)
        
        # Step 3: Enter search term
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(0.5)
        
        # Step 4: Press Enter
        send_keys("{ENTER}")
        
        # Step 5: Wait 3 seconds for results
        time.sleep(3)
        
        # Step 6: Tab 2 times to first result
        for _ in range(2):
            send_keys("{TAB}")
            time.sleep(0.3)
        
        # Step 7: Shift+Fn+F10 for context menu
        send_shift_f10()
        
        # Step 8: Wait 2 seconds
        time.sleep(2)
        
        # Step 9: Down arrow 5 times
        for _ in range(5):
            send_keys("{DOWN}")
            time.sleep(0.2)
        
        # Step 10: Enter to copy URL
        send_keys("{ENTER}")
        time.sleep(1)
        
        # Step 11: Extract copied URL
        url = get_clipboard()
        
        # Close Kinic
        send_keys("{ESC}")
        
        return jsonify({
            'success': bool(url),
            'query': query,
            'url': url,
            'message': f'Retrieved first URL for: {query}' if url else 'No URL found'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/close', methods=['POST'])
def close_kinic():
    """Close Kinic"""
    try:
        send_keys("{ESC}")
        return jsonify({'success': True, 'message': 'Closed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup', methods=['POST'])
def setup():
    """Update position"""
    try:
        data = request.get_json()
        config['kinic_x'] = data['x']
        config['kinic_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic API v4 - With Search & Retrieve")
    print("=" * 50)
    print(f"Config: Kinic at ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print("\nKey endpoint:")
    print("  POST /search-and-retrieve - Search and get first URL")
    print("\nExample:")
    print('  curl -X POST http://localhost:5004/search-and-retrieve \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"query":"code"}\'')
    print("\nRunning on http://localhost:5004")
    app.run(host='0.0.0.0', port=5004, debug=False)