#!/usr/bin/env python3
"""Test extraction from input/textarea field"""

import subprocess
import time
import json
import os

def windows_click(x, y):
    """Single click at position"""
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
║  TEST: EXTRACT FROM INPUT/TEXTAREA FIELD      ║
╚════════════════════════════════════════════════╝

The I-beam cursor indicates this is an input field.
Testing different selection methods...
""")

ai_x = config['ai_response_x']
ai_y = config['ai_response_y']

print(f"Using coordinates: ({ai_x}, {ai_y})")
print("\nMake sure Kinic has an AI response visible!")
input("Press Enter when ready...")

# Method 1: Click and Ctrl+A
print("\n1. Testing Click + Ctrl+A method...")
clear_clipboard()
windows_click(ai_x, ai_y)
time.sleep(1)
send_keys("^a")  # Select all in input field
time.sleep(1)
send_keys("^c")
time.sleep(1)
text1 = get_clipboard()
print(f"   Result: {len(text1)} chars captured")

# Method 2: Triple-click (might still work in some inputs)
print("\n2. Testing triple-click method...")
clear_clipboard()
time.sleep(2)
windows_click(ai_x, ai_y)
time.sleep(0.02)
windows_click(ai_x, ai_y)
time.sleep(0.02)
windows_click(ai_x, ai_y)
time.sleep(1)
send_keys("^c")
time.sleep(1)
text2 = get_clipboard()
print(f"   Result: {len(text2)} chars captured")

# Method 3: Click, then Shift+Ctrl+End
print("\n3. Testing Click + Shift+Ctrl+End method...")
clear_clipboard()
time.sleep(2)
windows_click(ai_x, ai_y)
time.sleep(1)
send_keys("^{HOME}")  # Go to start
time.sleep(0.5)
send_keys("^+{END}")  # Select to end
time.sleep(1)
send_keys("^c")
time.sleep(1)
text3 = get_clipboard()
print(f"   Result: {len(text3)} chars captured")

print("\n" + "="*60)
print("RESULTS:")
print("="*60)

methods = [
    ("Ctrl+A", text1),
    ("Triple-click", text2),
    ("Ctrl+Shift+End", text3)
]

best_method = None
best_length = 0

for method, text in methods:
    if text and text != "[empty]":
        print(f"\n{method}: {len(text)} characters")
        print(f"Preview: {text[:100]}...")
        if len(text) > best_length:
            best_method = method
            best_length = len(text)

if best_method:
    print(f"\n✅ BEST METHOD: {best_method} with {best_length} characters")
    print("\nFull text from best method:")
    print("-" * 40)
    if best_method == "Ctrl+A":
        print(text1)
    elif best_method == "Triple-click":
        print(text2)
    else:
        print(text3)
    print("-" * 40)
else:
    print("\n❌ No method captured text successfully")

print("\nClosing Kinic...")
send_keys("{ESC}")