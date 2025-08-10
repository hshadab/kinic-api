#!/usr/bin/env python3
"""Focus Chrome, then extract Venice AI response"""

import subprocess
import time
import json
import os

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
        Write-Host "Chrome focused"
    }
    """
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

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
    Start-Sleep -Milliseconds 50
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

def get_clipboard_safe():
    """Get clipboard with safe encoding"""
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

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════╗
║   FOCUS CHROME AND EXTRACT VENICE AI          ║
╚════════════════════════════════════════════════╝
""")

ai_x = config['ai_response_x']
ai_y = config['ai_response_y']

print("1. Focusing Chrome window...")
focus_chrome()
time.sleep(2)

print(f"2. Clicking AI response area at ({ai_x}, {ai_y})...")
# Single click first to ensure focus
windows_click(ai_x, ai_y)
time.sleep(1)

print("3. Triple-clicking to select all...")
# Triple click with very fast timing
windows_click(ai_x, ai_y)
time.sleep(0.02)  # 20ms
windows_click(ai_x, ai_y)
time.sleep(0.02)  # 20ms
windows_click(ai_x, ai_y)

print("4. Waiting for selection...")
time.sleep(2)

print("5. Copying with Ctrl+C...")
send_keys("^c")

print("6. Waiting for copy to complete...")
time.sleep(2)

print("7. Reading clipboard...")
text = get_clipboard_safe()

print("\n" + "="*60)

if text and len(text) > 20:
    print(f"✅ SUCCESS! Captured {len(text)} characters")
    print("\nVenice AI Response:")
    print("-"*40)
    print(text)
    print("-"*40)
    
    # Save it
    with open("venice-ai-response-final.txt", "w", encoding='utf-8') as f:
        f.write("Venice AI Response from Kinic\n")
        f.write("="*40 + "\n")
        f.write(text)
    print("\n📄 Saved to venice-ai-response-final.txt")
else:
    print(f"❌ No substantial text captured")
    print(f"Clipboard: '{text}'")