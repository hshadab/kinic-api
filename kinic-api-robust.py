#!/usr/bin/env python3
"""Kinic API - Robust version with safety steps"""

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
    config = {
        'kinic_x': 1379, 
        'kinic_y': 101,
        'ai_response_x': 939,
        'ai_response_y': 833
    }

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
    $chrome = Get-Process chrome | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object -First 1
    if ($chrome) {
        [Win32]::SetForegroundWindow($chrome.MainWindowHandle)
    }
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def robust_action_wrapper(action_func):
    """Wrapper that adds safety steps before and after each action"""
    def wrapper(*args, **kwargs):
        # Step 1: Focus Chrome
        focus_chrome()
        time.sleep(0.5)
        
        # Step 2: Press ESC to close any existing Kinic popup
        send_keys("{ESC}")
        time.sleep(0.5)
        
        # Step 3: Perform the action
        result = action_func(*args, **kwargs)
        
        # Step 4: Close Kinic at the end (give time for action to complete first)
        time.sleep(1)
        send_keys("{ESC}")
        
        return result
    return wrapper

def get_clipboard():
    """Get clipboard content with proper encoding handling"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=5
    )
    
    return result.stdout.strip() if result.stdout else None

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'version': 'robust',
        'config': config,
        'endpoints': {
            'POST /save': 'Save current page (robust)',
            'POST /search-and-retrieve': 'Search and get first URL (robust)',
            'POST /search-ai-extract': 'Search and extract AI text (robust)',
            'POST /click': 'Click Kinic button',
            'POST /close': 'Close Kinic',
            'POST /setup-kinic': 'Set Kinic position',
            'POST /setup-ai': 'Set AI response position'
        }
    })

@app.route('/save', methods=['POST'])
def save_page():
    """Robust save with proper 2s minimum delays"""
    try:
        # Focus Chrome (2s delay)
        focus_chrome()
        time.sleep(2)
        
        # Close any existing Kinic popup (2s delay)
        send_keys("{ESC}")
        time.sleep(2)
        
        # Open Kinic (3s delay for full load)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Navigate to save button with Shift+Tab (2s delay)
        send_keys("+{TAB}")
        time.sleep(2)
        
        # Press Enter to save (2s delay for save to process)
        send_keys("{ENTER}")
        time.sleep(2)
        
        # Close Kinic
        send_keys("{ESC}")
        
        return jsonify({'success': True, 'message': 'Page saved (robust with proper timing)'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-and-retrieve', methods=['POST'])
def search_and_retrieve():
    """Robust search and retrieve"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Focus Chrome (2s delay)
        focus_chrome()
        time.sleep(2)
        
        # Close any existing Kinic popup (2s delay)
        send_keys("{ESC}")
        time.sleep(2)
        
        # Open Kinic (3s delay for full load)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Tab to search field (0.5s between tabs, 2s after)
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(2)
        
        # Type search query (2s delay after)
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(2)
        send_keys("{ENTER}")
        
        # Wait for search results (4s)
        time.sleep(4)
        
        # Tab to first result (0.5s between, 2s after)
        for _ in range(2):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(2)
        
        # Open context menu (3s for menu to render)
        send_keys("+{F10}")
        time.sleep(3)
        
        # Navigate to copy URL (0.3s between, 2s after)
        for _ in range(5):
            send_keys("{DOWN}")
            time.sleep(0.3)
        time.sleep(2)
        
        send_keys("{ENTER}")
        time.sleep(2)
        
        # Get URL from clipboard
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
        send_keys("{ESC}")  # Make sure to close Kinic on error
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-ai-extract', methods=['POST'])
def search_ai_extract():
    """Robust search and AI text extraction"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Check AI response position is set
        if not config.get('ai_response_x') or not config.get('ai_response_y'):
            return jsonify({
                'success': False, 
                'error': 'AI response position not set. Use /setup-ai first'
            }), 400
        
        # Focus Chrome (2s delay)
        focus_chrome()
        time.sleep(2)
        
        # Close any existing Kinic popup (2s delay)
        send_keys("{ESC}")
        time.sleep(2)
        
        # Open Kinic (3s delay for full load)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Search (0.5s between tabs, 2s after)
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(2)
        
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(2)
        send_keys("{ENTER}")
        
        # Wait for search results (4s)
        time.sleep(4)
        
        # Click AI button (0.5s between tabs, 2s after)
        for _ in range(5):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(2)
        send_keys("{ENTER}")
        
        # Wait for AI response (10s for generation)
        time.sleep(10)
        
        # Triple-click to select AI text (VERY fast like real triple-click)
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.02)  # 20ms between clicks (ultra fast)
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.02)  # 20ms between clicks (ultra fast)
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(2)  # Wait after selection
        
        # Copy to clipboard (2s delay)
        send_keys("^c")
        time.sleep(2)
        
        # Get AI response
        ai_response = get_clipboard()
        
        # Close Kinic
        send_keys("{ESC}")
        
        return jsonify({
            'success': bool(ai_response),
            'query': query,
            'ai_response': ai_response,
            'message': f'AI response extracted for: {query}' if ai_response else 'No AI response captured'
        })
        
    except Exception as e:
        send_keys("{ESC}")  # Make sure to close Kinic on error
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/click', methods=['POST'])
def click_kinic():
    """Simple click without closing"""
    try:
        focus_chrome()
        time.sleep(2)  # Proper 2s delay
        windows_click(config['kinic_x'], config['kinic_y'])
        return jsonify({'success': True, 'message': f"Clicked at ({config['kinic_x']}, {config['kinic_y']})"})
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

@app.route('/setup-kinic', methods=['POST'])
def setup_kinic():
    """Update Kinic button position"""
    try:
        data = request.get_json()
        config['kinic_x'] = data['x']
        config['kinic_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup-ai', methods=['POST'])
def setup_ai():
    """Update AI response position"""
    try:
        data = request.get_json()
        config['ai_response_x'] = data['x']
        config['ai_response_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic API - ROBUST VERSION")
    print("=" * 60)
    print("✅ Safety features enabled:")
    print("  • Focus Chrome before each action")
    print("  • Press ESC to close existing popups")
    print("  • Close Kinic after each action")
    print("\nConfiguration:")
    print(f"  Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print(f"  AI response: ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
    print("\nRunning on http://localhost:5006")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5006, debug=False)