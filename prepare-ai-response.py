#!/usr/bin/env python3
"""Prepare Kinic with an AI response"""

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

def focus_chrome():
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

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════╗
║     PREPARING AI RESPONSE IN KINIC            ║
╚════════════════════════════════════════════════╝
""")

print("1. Focusing Chrome...")
focus_chrome()
time.sleep(2)

print("2. Closing any existing Kinic popup...")
send_keys("{ESC}")
time.sleep(2)

print("3. Opening Kinic...")
windows_click(config['kinic_x'], config['kinic_y'])
time.sleep(3)

print("4. Searching for 'JavaScript tutorial'...")
for _ in range(4):
    send_keys("{TAB}")
    time.sleep(0.5)
time.sleep(2)

send_keys("JavaScript tutorial")
time.sleep(2)
send_keys("{ENTER}")

print("5. Waiting for search results...")
time.sleep(4)

print("6. Clicking AI button...")
for _ in range(5):
    send_keys("{TAB}")
    time.sleep(0.5)
time.sleep(2)
send_keys("{ENTER}")

print("7. Waiting 10 seconds for AI response...")
for i in range(10, 0, -1):
    print(f"   {i}...", end='\r')
    time.sleep(1)

print("\n\n✅ AI response should now be visible in Kinic!")
print("   DO NOT CLOSE KINIC")
print("\nNow run: python test-triple-click-timing.py")