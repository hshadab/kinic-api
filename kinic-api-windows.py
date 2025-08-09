#!/usr/bin/env python3
"""Kinic API Server - Windows-native version that actually works"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Load or create config
config_file = os.path.expanduser("~/.kinic/config.json")
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    config = {
        'kinic_x': 904,
        'kinic_y': 96,
        'ai_response_x': None,
        'ai_response_y': None
    }

def save_config():
    """Save config to file"""
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def windows_click(x, y):
    """Click using Windows PowerShell - this actually works!"""
    ps_script = f"""
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        using System.Threading;
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
    Start-Sleep -Milliseconds 50
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 50
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    """
    
    try:
        subprocess.run(
            ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", 
             "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True, text=True, timeout=5
        )
        return True
    except Exception as e:
        print(f"Click failed: {e}")
        return False

def windows_type(text):
    """Type text using Windows PowerShell"""
    # Escape special characters for PowerShell
    text = text.replace('"', '`"').replace("'", "''")
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{text}")
    """
    
    try:
        subprocess.run(
            ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
             "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True, text=True, timeout=5
        )
        return True
    except:
        return False

def windows_key(key):
    """Send keyboard key using Windows PowerShell"""
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{{{key}}}")
    """
    
    try:
        subprocess.run(
            ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
             "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True, text=True, timeout=5
        )
        return True
    except:
        return False

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
            'POST /click-kinic': 'Just click the Kinic button',
            'POST /save': 'Save current page to Kinic',
            'POST /search': 'Search in Kinic - Body: {"query": "your search"}',
            'POST /setup/kinic': 'Set Kinic button position - Body: {"x": 904, "y": 96}',
            'POST /setup/ai-response': 'Set AI response position - Body: {"x": 600, "y": 400}'
        }
    })

@app.route('/click-kinic', methods=['POST'])
def click_kinic():
    """Just open Kinic"""
    try:
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        return jsonify({'success': True, 'message': f"Clicked Kinic at ({config['kinic_x']}, {config['kinic_y']})"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
    """Save current page to Kinic"""
    try:
        # Focus Chrome and click Kinic
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)  # Wait for Kinic to open
        
        # Shift+Tab then Enter to save
        windows_key("SHIFT+TAB")
        time.sleep(0.5)
        windows_key("ENTER")
        
        return jsonify({'success': True, 'message': 'Page saved to Kinic'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_kinic():
    """Search in Kinic"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Focus Chrome and click Kinic
        focus_chrome()
        time.sleep(0.3)
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)  # Wait for Kinic to open
        
        # Tab to search field (4 times)
        for _ in range(4):
            windows_key("TAB")
            time.sleep(0.2)
        
        # Type query and search
        windows_type(query)
        time.sleep(0.5)
        windows_key("ENTER")
        
        return jsonify({'success': True, 'message': f'Searched for: {query}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup/kinic', methods=['POST'])
def setup_kinic():
    """Set Kinic button position"""
    try:
        data = request.get_json()
        config['kinic_x'] = data['x']
        config['kinic_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup/ai-response', methods=['POST'])
def setup_ai_response():
    """Set AI response text position"""
    try:
        data = request.get_json()
        config['ai_response_x'] = data['x']
        config['ai_response_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic Windows API Server")
    print("=" * 50)
    print(f"Config: Kinic at ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print("\nEndpoints:")
    print("  POST http://localhost:5002/click-kinic - Open Kinic")
    print("  POST http://localhost:5002/save - Save current page")
    print('  POST http://localhost:5002/search -d \'{"query":"test"}\'')
    print("\nServer running on http://localhost:5002")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5002, debug=False)