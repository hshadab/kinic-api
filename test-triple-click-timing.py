#!/usr/bin/env python3
"""Test triple-click with better timing"""

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
    Start-Sleep -Milliseconds 50
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
    return result.stdout.strip() if result.stdout else ""

def clear_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

print("""
╔════════════════════════════════════════════════╗
║     TRIPLE-CLICK TIMING TEST                  ║
╚════════════════════════════════════════════════╝

Testing different triple-click timings...
Make sure Kinic has an AI response visible!
""")

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

ai_x = config['ai_response_x']
ai_y = config['ai_response_y']

print(f"AI Response position: ({ai_x}, {ai_y})")

# Test 1: Fast triple-click (200ms between clicks)
print("\n1. Testing FAST triple-click (200ms gaps)...")
clear_clipboard()
windows_click(ai_x, ai_y)
time.sleep(0.2)
windows_click(ai_x, ai_y)
time.sleep(0.2)
windows_click(ai_x, ai_y)
time.sleep(1)
send_keys("^c")
time.sleep(1)
text1 = get_clipboard()
print(f"   Result: {len(text1)} characters captured")

# Test 2: Medium triple-click (400ms between clicks)
print("\n2. Testing MEDIUM triple-click (400ms gaps)...")
clear_clipboard()
time.sleep(2)  # Let selection clear
windows_click(ai_x, ai_y)
time.sleep(0.4)
windows_click(ai_x, ai_y)
time.sleep(0.4)
windows_click(ai_x, ai_y)
time.sleep(1)
send_keys("^c")
time.sleep(1)
text2 = get_clipboard()
print(f"   Result: {len(text2)} characters captured")

# Test 3: Slow triple-click (600ms between clicks)
print("\n3. Testing SLOW triple-click (600ms gaps)...")
clear_clipboard()
time.sleep(2)  # Let selection clear
windows_click(ai_x, ai_y)
time.sleep(0.6)
windows_click(ai_x, ai_y)
time.sleep(0.6)
windows_click(ai_x, ai_y)
time.sleep(1)
send_keys("^c")
time.sleep(1)
text3 = get_clipboard()
print(f"   Result: {len(text3)} characters captured")

print("\n" + "="*60)
print("RESULTS:")
print("="*60)

if text1:
    print(f"Fast (200ms): {len(text1)} chars")
    print(f"  Preview: {text1[:100]}...")
if text2:
    print(f"Medium (400ms): {len(text2)} chars")
    print(f"  Preview: {text2[:100]}...")
if text3:
    print(f"Slow (600ms): {len(text3)} chars")
    print(f"  Preview: {text3[:100]}...")

if not (text1 or text2 or text3):
    print("❌ No text captured with any timing!")
    print("\nPossible issues:")
    print("- AI response coordinates might be off")
    print("- Need to click exactly in the text area")
    print("- AI response might not be visible")
else:
    # Find best timing
    best = max([(len(text1), "Fast 200ms"), (len(text2), "Medium 400ms"), (len(text3), "Slow 600ms")])
    print(f"\n✅ Best result: {best[1]} with {best[0]} characters")

print("="*60)

# Close Kinic
send_keys("{ESC}")