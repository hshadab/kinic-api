#!/usr/bin/env python3
"""Test AI extraction with better selection method"""

import subprocess
import time

def send_keys(keys):
    ps = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps], capture_output=True)

def click(x, y):
    ps = f'''
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class W {{
            [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
            [DllImport("user32.dll")] public static extern void mouse_event(uint f, int x, int y, uint d, int e);
        }}
"@
    [W]::SetCursorPos({x},{y})
    [W]::mouse_event(2,0,0,0,0)
    [W]::mouse_event(4,0,0,0,0)
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps], capture_output=True)

print("Testing AI text extraction...")

# Open Kinic
print("1. Opening Kinic...")
click(1387, 99)
time.sleep(2)

# Search
print("2. Searching for 'technology'...")
for _ in range(4):
    send_keys("{TAB}")
    time.sleep(0.2)
send_keys("technology")
send_keys("{ENTER}")
time.sleep(3)

# Click AI button
print("3. Clicking AI button...")
for _ in range(5):
    send_keys("{TAB}")
    time.sleep(0.2)
send_keys("{ENTER}")

print("4. Waiting 10 seconds for AI response...")
time.sleep(10)

# Click in AI response area
print("5. Clicking AI response area at (1002, 821)...")
click(1002, 821)
time.sleep(0.5)

# Try Ctrl+A to select all
print("6. Selecting all text with Ctrl+A...")
send_keys("^a")
time.sleep(0.5)

# Copy
print("7. Copying with Ctrl+C...")
send_keys("^c")
time.sleep(1)

# Get clipboard
ps = '''
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Clipboard]::GetText()
'''
result = subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps], capture_output=True, text=True)

print("\n" + "=" * 60)
print("AI RESPONSE:")
print("-" * 60)
print(result.stdout if result.stdout else "No text captured")
print("=" * 60)

# Close Kinic
send_keys("{ESC}")