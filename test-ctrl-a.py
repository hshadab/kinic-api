#!/usr/bin/env python3
"""Test using Ctrl+A instead of triple-click"""

import subprocess
import time
import json
import os

def windows_click(x, y):
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

print("""
╔════════════════════════════════════════════════╗
║     TEST CTRL+A SELECTION METHOD              ║
╚════════════════════════════════════════════════╝

Assuming Kinic is open with AI response visible...
""")

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print(f"1. Clicking in AI area at ({config['ai_response_x']}, {config['ai_response_y']})...")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(2)

print("2. Pressing Ctrl+A to select all...")
send_keys("^a")
time.sleep(2)

print("3. Copying with Ctrl+C...")
send_keys("^c")
time.sleep(2)

print("4. Closing Kinic...")
send_keys("{ESC}")

print("\nDone! Check if text was selected and copied.")