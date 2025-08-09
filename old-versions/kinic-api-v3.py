#!/usr/bin/env python3
"""Kinic API v3 - With reliable clicking that handles near misses"""

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
    config = {'kinic_x': 962, 'kinic_y': 98}

def save_config():
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def windows_click_area(x, y, radius=2):
    """Click in a small area around the target to handle near misses"""
    positions = [(x, y)]  # Center first
    
    # Add cross pattern
    if radius > 0:
        positions.extend([
            (x - radius, y),  # left
            (x + radius, y),  # right
            (x, y - radius),  # up
            (x, y + radius),  # down
        ])
    
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
    """
    
    # Try each position
    for px, py in positions:
        ps_script += f"""
    [Win32]::SetCursorPos({px}, {py})
    Start-Sleep -Milliseconds 100
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 50
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 300
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    return True

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

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'config': config,
        'endpoints': {
            'POST /click': 'Click Kinic (with auto-correction for near misses)',
            'POST /save': 'Save current page',
            'POST /search': 'Search - Body: {"query": "text"}',
            'POST /close': 'Close Kinic extension',
            'POST /setup': 'Set position - Body: {"x": 962, "y": 98}',
            'GET /test-grid': 'Test click in grid pattern'
        }
    })

@app.route('/click', methods=['POST'])
def click_kinic():
    """Click Kinic with tolerance for near misses"""
    try:
        focus_chrome()
        time.sleep(0.3)
        
        # Try clicking with a small radius to handle near misses
        windows_click_area(config['kinic_x'], config['kinic_y'], radius=2)
        
        return jsonify({
            'success': True,
            'message': f"Clicked Kinic area around ({config['kinic_x']}, {config['kinic_y']})"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
    """Save current page to Kinic"""
    try:
        # Click Kinic
        focus_chrome()
        time.sleep(0.3)
        windows_click_area(config['kinic_x'], config['kinic_y'], radius=2)
        time.sleep(2)
        
        # Save with Shift+Tab, Enter
        send_keys("+{TAB}")
        time.sleep(0.5)
        send_keys("{ENTER}")
        
        return jsonify({'success': True, 'message': 'Page saved'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    """Search in Kinic"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query'}), 400
        
        # Click Kinic
        focus_chrome()
        time.sleep(0.3)
        windows_click_area(config['kinic_x'], config['kinic_y'], radius=2)
        time.sleep(2)
        
        # Tab to search (4 times)
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.2)
        
        # Type and search
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(0.5)
        send_keys("{ENTER}")
        
        return jsonify({'success': True, 'message': f'Searched: {query}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/close', methods=['POST'])
def close_kinic():
    """Close Kinic extension"""
    try:
        send_keys("{ESC}")
        return jsonify({'success': True, 'message': 'Closed Kinic'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup', methods=['POST'])
def setup():
    """Update Kinic position"""
    try:
        data = request.get_json()
        config['kinic_x'] = data['x']
        config['kinic_y'] = data['y']
        save_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test-grid', methods=['GET'])
def test_grid():
    """Test clicking in a grid pattern"""
    try:
        focus_chrome()
        time.sleep(0.3)
        
        base_x, base_y = config['kinic_x'], config['kinic_y']
        tested = []
        
        for dx in [-4, -2, 0, 2, 4]:
            for dy in [-4, -2, 0, 2, 4]:
                x, y = base_x + dx, base_y + dy
                windows_click_area(x, y, radius=0)
                tested.append((x, y))
                time.sleep(1)
        
        return jsonify({
            'success': True,
            'message': f'Tested {len(tested)} positions around ({base_x}, {base_y})',
            'positions': tested
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic API v3 - With Near-Miss Correction")
    print("=" * 50)
    print(f"Config: Kinic at ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print("\nThis version clicks in a small area to handle near misses")
    print("\nEndpoints:")
    print("  POST /click - Click Kinic (auto-corrects near misses)")
    print("  POST /save - Save current page")
    print("  POST /search - Search in Kinic")
    print("  POST /close - Close Kinic")
    print("  GET /test-grid - Test grid pattern")
    print("\nRunning on http://localhost:5003")
    app.run(host='0.0.0.0', port=5003, debug=False)