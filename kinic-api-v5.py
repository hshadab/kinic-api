#!/usr/bin/env python3
"""Kinic API v5 - Complete with AI text extraction"""

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
        'kinic_x': 959, 
        'kinic_y': 98,
        'ai_response_x': 555,
        'ai_response_y': 576
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
            'POST /search-and-retrieve': 'Search and get first URL - Body: {"query": "text"}',
            'POST /search-ai-extract': 'Search, run AI, and extract text - Body: {"query": "text"}',
            'POST /close': 'Close Kinic',
            'POST /setup-kinic': 'Set Kinic position - Body: {"x": 959, "y": 98}',
            'POST /setup-ai': 'Set AI response position - Body: {"x": 555, "y": 576}'
        }
    })

@app.route('/search-ai-extract', methods=['POST'])
def search_ai_extract():
    """Search, run AI, and extract the AI response text"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Check if AI response position is set
        if not config.get('ai_response_x') or not config.get('ai_response_y'):
            return jsonify({
                'success': False, 
                'error': 'AI response position not set. Use /setup-ai first'
            }), 400
        
        # Step 1: Open Kinic
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Step 2: Search
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.2)
        
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(0.5)
        send_keys("{ENTER}")
        
        # Step 3: Wait for search results
        time.sleep(3)
        
        # Step 4: Click AI button (5 tabs from search)
        for _ in range(5):
            send_keys("{TAB}")
            time.sleep(0.2)
        send_keys("{ENTER}")
        
        # Step 5: Wait for AI response to generate
        time.sleep(8)  # Adjust based on typical response time
        
        # Step 6: Triple-click in AI response area to select all text
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.2)
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.2)
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.5)
        
        # Step 7: Copy to clipboard
        send_keys("^c")
        time.sleep(1)
        
        # Step 9: Get the AI response text
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
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-and-retrieve', methods=['POST'])
def search_and_retrieve():
    """Search and retrieve first URL"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.2)
        
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(0.5)
        send_keys("{ENTER}")
        time.sleep(3)
        
        for _ in range(2):
            send_keys("{TAB}")
            time.sleep(0.3)
        
        send_shift_f10()
        time.sleep(2)
        
        for _ in range(5):
            send_keys("{DOWN}")
            time.sleep(0.2)
        
        send_keys("{ENTER}")
        time.sleep(1)
        
        url = get_clipboard()
        send_keys("{ESC}")
        
        return jsonify({
            'success': bool(url),
            'query': query,
            'url': url,
            'message': f'Retrieved first URL for: {query}' if url else 'No URL found'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/click', methods=['POST'])
def click_kinic():
    try:
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        return jsonify({'success': True, 'message': f"Clicked at ({config['kinic_x']}, {config['kinic_y']})"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
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


@app.route('/close', methods=['POST'])
def close_kinic():
    try:
        send_keys("{ESC}")
        return jsonify({'success': True, 'message': 'Closed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup-kinic', methods=['POST'])
def setup_kinic():
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
    try:
        data = request.get_json()
        config['ai_response_x'] = data['x']
        config['ai_response_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic API v5 - Complete with AI Text Extraction")
    print("=" * 60)
    print("Configuration:")
    print(f"  Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print(f"  AI response: ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
    print("\nKey endpoints:")
    print("  POST /search-and-retrieve - Search and get first URL")
    print("  POST /search-ai-extract - Search, AI, and extract text")
    print("\nExamples:")
    print('  curl -X POST http://localhost:5005/search-ai-extract \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"query":"explain quantum computing"}\'')
    print("\nRunning on http://localhost:5005")
    app.run(host='0.0.0.0', port=5005, debug=False)