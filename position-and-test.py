#!/usr/bin/env python3
"""Position mouse on AI response, capture coords, and test immediately"""

import subprocess
import time

def get_mouse_position():
    """Get current mouse position"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        using System.Drawing;
        
        public class MouseInfo {
            [DllImport("user32.dll")]
            public static extern bool GetCursorPos(out POINT lpPoint);
            
            [StructLayout(LayoutKind.Sequential)]
            public struct POINT {
                public int X;
                public int Y;
            }
            
            public static string GetPosition() {
                POINT point;
                GetCursorPos(out point);
                return point.X + "," + point.Y;
            }
        }
'@
    [MouseInfo]::GetPosition()
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    if result.stdout:
        coords = result.stdout.strip().split(',')
        return int(coords[0]), int(coords[1])
    return None, None

def triple_click_at_current():
    """Triple click at current mouse position"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);
            public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
            public const uint MOUSEEVENTF_LEFTUP = 0x0004;
        }
'@
    # Triple click
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 10
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 20
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 10
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 20
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 10
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    """
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def send_keys(keys):
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

def get_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    '''
    result = subprocess.run(
        ['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], 
        capture_output=True, 
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return result.stdout.strip() if result.stdout else ""

print("""
╔════════════════════════════════════════════════════════════╗
║     POSITION MOUSE AND TEST EXTRACTION                    ║
╠════════════════════════════════════════════════════════════╣
║  1. Position your mouse on the Venice AI response text    ║
║  2. Press Enter                                           ║
║  3. Script will capture position and test extraction      ║
╚════════════════════════════════════════════════════════════╝
""")

input("\nPosition mouse on Venice AI text and press Enter...")

print("\nCapturing position in 2 seconds - keep mouse still!")
time.sleep(2)

x, y = get_mouse_position()
print(f"✅ Captured position: ({x}, {y})")

print("\nTesting extraction at this exact position...")

print("1. Triple-clicking...")
triple_click_at_current()

print("2. Waiting for selection...")
time.sleep(2)

print("3. Copying...")
send_keys("^c")

print("4. Waiting for copy...")
time.sleep(2)

print("5. Reading clipboard...")
text = get_clipboard()

print("\n" + "="*60)
print("RESULT:")
print("="*60)

if text and len(text) > 20:
    print(f"✅ SUCCESS! Captured {len(text)} characters at ({x}, {y})")
    print("\nVenice AI Response:")
    print("-"*40)
    print(text[:500])  # First 500 chars
    if len(text) > 500:
        print("... (truncated)")
    print("-"*40)
    
    # Save full text
    with open("venice-full-response.txt", "w", encoding='utf-8') as f:
        f.write(f"Position: ({x}, {y})\n")
        f.write(f"Length: {len(text)} characters\n\n")
        f.write(text)
    print("\n📄 Full response saved to venice-full-response.txt")
    
    # Update config
    import json
    import os
    config_file = os.path.expanduser("~/.kinic/config.json")
    with open(config_file, 'r') as f:
        config = json.load(f)
    config['ai_response_x'] = x
    config['ai_response_y'] = y
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Updated config with new position: ({x}, {y})")
    
else:
    print(f"❌ Failed at position ({x}, {y})")
    print(f"Clipboard: '{text[:100]}...'" if text else "Clipboard: empty")