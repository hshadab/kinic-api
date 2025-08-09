#!/usr/bin/env python3
"""Manual step-by-step AI test to see what's happening"""

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

def get_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    '''
    result = subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "[empty]"

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════╗
║     MANUAL AI TEXT SELECTION TEST             ║
╚════════════════════════════════════════════════╝

This will manually test the AI text selection.
Make sure Kinic has an AI response visible!
""")

print("\n1. First, let's open Kinic and search...")
windows_click(config['kinic_x'], config['kinic_y'])
time.sleep(3)

print("2. Searching for 'Python'...")
for _ in range(4):
    send_keys("{TAB}")
    time.sleep(0.5)
time.sleep(1)

send_keys("Python")
time.sleep(1)
send_keys("{ENTER}")

print("3. Waiting for search results...")
time.sleep(4)

print("4. Clicking AI button...")
for _ in range(5):
    send_keys("{TAB}")
    time.sleep(0.5)
time.sleep(1)
send_keys("{ENTER}")

print("5. Waiting 10 seconds for AI to generate response...")
for i in range(10, 0, -1):
    print(f"   {i}...", end='\r')
    time.sleep(1)

print("\n6. Now trying to select AI text...")
print(f"   Position: ({config['ai_response_x']}, {config['ai_response_y']})")

print("   First click...")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.5)

print("   Second click...")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.5)

print("   Third click (should select all)...")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(2)

print("\n7. Copying with Ctrl+C...")
send_keys("^c")
time.sleep(2)

print("\n8. Checking clipboard...")
text = get_clipboard()

print("\n" + "="*60)
print("RESULT:")
print("="*60)
if text and text != "[empty]":
    print(f"✅ Captured {len(text)} characters:")
    print(text[:200])
    if len(text) > 200:
        print("...")
else:
    print("❌ No text captured")
    print("\nPOSSIBLE ISSUES:")
    print("- AI response position might be wrong")
    print("- Triple-click might not be selecting text")
    print("- AI might not have generated a response")
    
print("="*60)

# Close Kinic
send_keys("{ESC}")