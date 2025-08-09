#!/usr/bin/env python3
"""Auto save test - no input needed"""

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
    """Send keyboard keys"""
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def open_url(url):
    """Open URL in Chrome"""
    ps_script = f'Start-Process "chrome.exe" -ArgumentList "{url}"'
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
║     AUTOMATED KINIC SAVE TEST                 ║
╚════════════════════════════════════════════════╝
""")

# First open a page to save
url = "https://docs.python.org/3/library/random.html"
print(f"📄 Opening page: {url}")
open_url(url)

print("⏳ Waiting 5 seconds for page to load...")
time.sleep(5)

print(f"\n🎯 Starting save sequence with Kinic at ({config['kinic_x']}, {config['kinic_y']})")

print("\n1️⃣  Clicking Kinic button...")
windows_click(config['kinic_x'], config['kinic_y'])
print("   ✓ Clicked")

print("2️⃣  Waiting 2.5 seconds for Kinic to open...")
time.sleep(2.5)

print("3️⃣  Pressing Shift+Tab to focus save button...")
send_keys("+{TAB}")
print("   ✓ Sent Shift+Tab")

print("4️⃣  Waiting 0.8 seconds...")
time.sleep(0.8)

print("5️⃣  Pressing Enter to save...")
send_keys("{ENTER}")
print("   ✓ Sent Enter")

print("\n" + "="*50)
print("✅ SAVE SEQUENCE COMPLETE!")
print("="*50)
print(f"""
Please check Kinic now:
1. Click the Kinic icon again
2. Look for: {url}
3. It should be in your saved items

Did it save the page?
""")