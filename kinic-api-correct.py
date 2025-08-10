#!/usr/bin/env python3
"""
Kinic API - Correct Sequence
Implements the proper workflow: cursor must be moved into AI text field
"""

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

def get_clipboard():
    """Get clipboard content with proper encoding"""
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

def clear_clipboard():
    """Clear clipboard"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    """
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, timeout=5
    )

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'version': 'correct-sequence',
        'config': config,
        'endpoints': {
            'POST /ai-extract': 'Extract AI response with correct sequence',
            'POST /save': 'Save current page'
        },
        'sequence': [
            '1. Open Kinic',
            '2. Four tabs to search',
            '3. Enter search terms',
            '4. Press Enter',
            '5. Five tabs to AI button',
            '6. Enter to run AI',
            '7. Wait 5 seconds',
            '8. Move cursor into text field',
            '9. Triple click',
            '10. Ctrl+C',
            '11. Extract'
        ]
    })

@app.route('/ai-extract', methods=['POST'])
def ai_extract_correct():
    """AI extraction with the correct sequence"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # 1. Focus Chrome
        focus_chrome()
        time.sleep(2)
        
        # Close any existing popup
        send_keys("{ESC}")
        time.sleep(2)
        
        # 1. Open Kinic
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)  # Wait for Kinic to load
        
        # 2. Four tabs to search field
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(1)
        
        # 3. Enter search terms
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(1)
        
        # 4. Press Enter
        send_keys("{ENTER}")
        time.sleep(4)  # Wait for search results
        
        # 5. Five tabs to AI button
        for _ in range(5):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(1)
        
        # 6. Enter to run AI
        send_keys("{ENTER}")
        
        # 7. Wait 10 seconds for AI generation (was 5, but AI needs more time)
        time.sleep(10)
        
        # 8. CRITICAL: Move cursor into text field
        # This is the key step - we must click in the AI response area
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(1)
        
        # 9. Triple click (3 clicks with fast timing)
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.02)  # 20ms
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.02)  # 20ms
        windows_click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(1)  # Wait for selection
        
        # 10. Control C
        clear_clipboard()  # Clear first
        send_keys("^c")
        time.sleep(2)  # Wait for copy
        
        # 11. Extract
        ai_response = get_clipboard()
        
        # Close Kinic
        send_keys("{ESC}")
        
        # Validate response
        success = bool(ai_response and len(ai_response) > 50)
        
        return jsonify({
            'success': success,
            'query': query,
            'ai_response': ai_response if ai_response else "",
            'response_length': len(ai_response) if ai_response else 0,
            'message': f'Extracted {len(ai_response)} chars' if success else 'Extraction failed'
        })
        
    except Exception as e:
        send_keys("{ESC}")  # Try to close Kinic
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
    """Save current page"""
    try:
        focus_chrome()
        time.sleep(2)
        
        send_keys("{ESC}")
        time.sleep(2)
        
        windows_click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        send_keys("+{TAB}")  # Shift+Tab to save button
        time.sleep(2)
        
        send_keys("{ENTER}")
        time.sleep(2)
        
        send_keys("{ESC}")
        
        return jsonify({'success': True, 'message': 'Page saved'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║        🎯 KINIC API - CORRECT SEQUENCE                    ║
╠════════════════════════════════════════════════════════════╣
║  Implements the proper workflow:                          ║
║  1. Open Kinic                                            ║
║  2. Four tabs → search                                    ║
║  3. Enter search terms                                    ║
║  4. Press Enter                                           ║
║  5. Five tabs → AI button                                 ║
║  6. Enter to run AI                                       ║
║  7. Wait 5 seconds                                        ║
║  8. ✨ Move cursor into text field (CRITICAL!)           ║
║  9. Triple click                                          ║
║  10. Ctrl+C                                               ║
║  11. Extract                                              ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Configuration:")
    print(f"  Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print(f"  AI response:  ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
    print(f"\nRunning on http://localhost:5008")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5008, debug=False)