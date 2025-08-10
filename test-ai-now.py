#!/usr/bin/env python3
"""Open Kinic, search, get AI response, and test extraction methods"""

import subprocess
import time
import json
import os

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
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

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

def get_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    '''
    result = subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "[empty]"

def clear_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════╗
║     FULL AI SEARCH AND EXTRACTION TEST        ║
╚════════════════════════════════════════════════╝
""")

print("Configuration:")
print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
print(f"  AI response:  ({config['ai_response_x']}, {config['ai_response_y']})")

# Since Kinic is already open, just search
print("\n1. Searching for 'Venice Italy'...")
# Tab to search field
for i in range(4):
    send_keys("{TAB}")
    time.sleep(0.5)
time.sleep(2)

# Type search
send_keys("Venice Italy")
time.sleep(2)
send_keys("{ENTER}")

print("2. Waiting for search results...")
time.sleep(4)

print("3. Clicking AI button...")
# Tab to AI button
for i in range(5):
    send_keys("{TAB}")
    time.sleep(0.5)
time.sleep(2)
send_keys("{ENTER}")

print("4. Waiting 10 seconds for AI response...")
for i in range(10, 0, -1):
    print(f"   {i}...", end='\r')
    time.sleep(1)

print("\n\nNow testing extraction methods:")
print("="*60)

# Method 1: Triple-click (you said this works)
print("\nMETHOD 1: Triple-click")
clear_clipboard()
print(f"  Clicking at ({config['ai_response_x']}, {config['ai_response_y']})")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.02)  # 20ms
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.02)  # 20ms
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(2)
print("  Copying...")
send_keys("^c")
time.sleep(2)
text1 = get_clipboard()
print(f"  Result: {len(text1)} chars")
if text1:
    print(f"  Preview: {text1[:100]}...")

# Method 2: Click + Ctrl+A
print("\nMETHOD 2: Click + Ctrl+A")
clear_clipboard()
time.sleep(2)
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(1)
send_keys("^a")
time.sleep(1)
send_keys("^c")
time.sleep(2)
text2 = get_clipboard()
print(f"  Result: {len(text2)} chars")
if text2:
    print(f"  Preview: {text2[:100]}...")

# Method 3: Focus field and get all
print("\nMETHOD 3: Click, Home, Shift+End")
clear_clipboard()
time.sleep(2)
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(1)
send_keys("{HOME}")
time.sleep(0.5)
send_keys("+{END}")
time.sleep(1)
send_keys("^c")
time.sleep(2)
text3 = get_clipboard()
print(f"  Result: {len(text3)} chars")
if text3:
    print(f"  Preview: {text3[:100]}...")

print("\n" + "="*60)
print("FINAL RESULTS:")
print("="*60)

if text1 and len(text1) > 50:
    print(f"\n✅ Triple-click worked! ({len(text1)} chars)")
    print("\nFull Venice AI response:")
    print("-"*40)
    print(text1)
    print("-"*40)
elif text2 and len(text2) > 50:
    print(f"\n✅ Ctrl+A worked! ({len(text2)} chars)")
    print("\nFull Venice AI response:")
    print("-"*40)
    print(text2)
    print("-"*40)
elif text3 and len(text3) > 50:
    print(f"\n✅ Home+Shift+End worked! ({len(text3)} chars)")
    print("\nFull Venice AI response:")
    print("-"*40)
    print(text3)
    print("-"*40)
else:
    print("\n❌ No method captured proper AI text")
    print(f"Method 1 (triple-click): {text1[:50] if text1 else 'empty'}")
    print(f"Method 2 (Ctrl+A): {text2[:50] if text2 else 'empty'}")
    print(f"Method 3 (Home+End): {text3[:50] if text3 else 'empty'}")

print("\nClosing Kinic...")
send_keys("{ESC}")