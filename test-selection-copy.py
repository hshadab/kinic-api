#!/usr/bin/env python3
"""Test if selection and copy work correctly"""

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
║     TEST SELECTION AND COPY                   ║
╚════════════════════════════════════════════════╝

Make sure Kinic has an AI response visible!
""")

print(f"Using coordinates: ({config['ai_response_x']}, {config['ai_response_y']})")

# Clear clipboard first
print("\n1. Clearing clipboard...")
clear_clipboard()
initial = get_clipboard()
print(f"   Clipboard: '{initial}'")

print("\n2. Triple-clicking in 3 seconds...")
print("   Watch if text gets selected!")
time.sleep(3)

# Triple-click
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.02)
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.02)
windows_click(config['ai_response_x'], config['ai_response_y'])

print("   Triple-click done!")
print("\n3. Waiting 2 seconds (text should stay selected)...")
time.sleep(2)

print("\n4. Copying with Ctrl+C...")
send_keys("^c")

print("\n5. Waiting 2 seconds for copy to complete...")
time.sleep(2)

print("\n6. Checking clipboard...")
result = get_clipboard()

print("\n" + "="*60)
print("RESULTS:")
print("="*60)
print(f"Clipboard before: '{initial}'")
print(f"Clipboard after:  '{result}'")
print(f"Characters captured: {len(result)}")

if result and result != "[empty]" and result != initial:
    print("\n✅ SUCCESS! Text was copied")
    print("\nFirst 200 characters:")
    print("-" * 40)
    print(result[:200])
    if len(result) > 200:
        print("...")
    print("-" * 40)
else:
    print("\n❌ FAILED! No text was copied")
    print("\nPossible issues:")
    print("1. Text wasn't selected by triple-click")
    print("2. Selection was lost before copy")
    print("3. Copy command didn't work")
    print("4. Focus changed between selection and copy")

print("\nClosing Kinic...")
send_keys("{ESC}")