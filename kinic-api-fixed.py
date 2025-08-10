#!/usr/bin/env python3
"""
Kinic API - Fixed cursor movement
Ensures cursor is properly moved to AI text field
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

def move_cursor(x, y):
    """Just move cursor without clicking"""
    ps_script = f"""
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern bool SetCursorPos(int X, int Y);
        }}
'@
    [Win32]::SetCursorPos({x}, {y})
    Write-Output "Cursor moved to {x},{y}"
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    return f"Cursor moved to {x},{y}" in result.stdout

def click_at_position(x, y):
    """Move cursor and click"""
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
    # First ensure cursor is at position
    [Win32]::SetCursorPos({x}, {y})
    Start-Sleep -Milliseconds 200
    
    # Then click
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 50
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def triple_click_at_position(x, y):
    """Move cursor and triple-click"""
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
            
            public static void TripleClick(int x, int y) {{
                // Move cursor
                SetCursorPos(x, y);
                Thread.Sleep(500); // Wait half second for cursor to settle
                
                // First click
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                Thread.Sleep(10);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                
                Thread.Sleep(20); // 20ms between clicks
                
                // Second click
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                Thread.Sleep(10);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                
                Thread.Sleep(20); // 20ms between clicks
                
                // Third click
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                Thread.Sleep(10);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
            }}
        }}
'@
    [Win32]::TripleClick({x}, {y})
    Write-Output "Triple-clicked at {x},{y}"
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    return "Triple-clicked" in result.stdout

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
    """Get clipboard content"""
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
        'version': 'fixed-cursor',
        'config': config,
        'endpoints': {
            'POST /ai-extract': 'Extract AI with proper cursor movement',
            'POST /test-cursor': 'Test cursor movement'
        }
    })

@app.route('/test-cursor', methods=['POST'])
def test_cursor():
    """Test if cursor movement works"""
    try:
        # Move cursor to AI response position
        moved = move_cursor(config['ai_response_x'], config['ai_response_y'])
        
        return jsonify({
            'success': moved,
            'position': f"({config['ai_response_x']}, {config['ai_response_y']})",
            'message': 'Cursor moved' if moved else 'Failed to move cursor'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/ai-extract', methods=['POST'])
def ai_extract_fixed():
    """AI extraction with fixed cursor movement"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Step 1: Focus Chrome
        focus_chrome()
        time.sleep(2)
        
        # Close any existing popup
        send_keys("{ESC}")
        time.sleep(2)
        
        # Step 2: Open Kinic
        click_at_position(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Step 3: Four tabs to search
        for _ in range(4):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(1)
        
        # Step 4: Enter search terms
        send_keys(query.replace('{', '{{').replace('}', '}}'))
        time.sleep(1)
        
        # Step 5: Press Enter
        send_keys("{ENTER}")
        time.sleep(4)
        
        # Step 6: Five tabs to AI button
        for _ in range(5):
            send_keys("{TAB}")
            time.sleep(0.5)
        time.sleep(1)
        
        # Step 7: Enter to run AI
        send_keys("{ENTER}")
        
        # Step 8: Wait for AI generation
        time.sleep(10)
        
        # Step 9: CRITICAL - Move cursor to AI text field
        # First just move cursor without clicking
        cursor_moved = move_cursor(config['ai_response_x'], config['ai_response_y'])
        time.sleep(1)
        
        if not cursor_moved:
            # Try again with click
            click_at_position(config['ai_response_x'], config['ai_response_y'])
            time.sleep(1)
        
        # Step 10: Triple-click with cursor already in position
        clear_clipboard()
        triple_clicked = triple_click_at_position(config['ai_response_x'], config['ai_response_y'])
        time.sleep(2)
        
        # Step 11: Copy
        send_keys("^c")
        time.sleep(2)
        
        # Step 12: Extract
        ai_response = get_clipboard()
        
        # If triple-click didn't work, try click and Ctrl+A
        if not ai_response or len(ai_response) < 50:
            clear_clipboard()
            click_at_position(config['ai_response_x'], config['ai_response_y'])
            time.sleep(1)
            send_keys("^a")
            time.sleep(1)
            send_keys("^c")
            time.sleep(2)
            ai_response = get_clipboard()
        
        # Close Kinic
        send_keys("{ESC}")
        
        success = bool(ai_response and len(ai_response) > 50)
        
        return jsonify({
            'success': success,
            'query': query,
            'ai_response': ai_response if ai_response else "",
            'response_length': len(ai_response) if ai_response else 0,
            'cursor_moved': cursor_moved,
            'triple_clicked': triple_clicked,
            'message': f'Extracted {len(ai_response)} chars' if success else 'Extraction failed'
        })
        
    except Exception as e:
        send_keys("{ESC}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║        🎯 KINIC API - FIXED CURSOR MOVEMENT               ║
╠════════════════════════════════════════════════════════════╣
║  Fixes the cursor disappearing issue:                     ║
║  • Explicitly moves cursor to AI text field               ║
║  • Waits for cursor to settle before clicking             ║
║  • Triple-clicks with cursor in correct position          ║
║  • Falls back to Ctrl+A if needed                         ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Configuration:")
    print(f"  Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print(f"  AI response:  ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
    print(f"\nRunning on http://localhost:5009")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5009, debug=False)