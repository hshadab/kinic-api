#!/usr/bin/env python3
"""Test the exact save sequence: Open Kinic, Shift+Tab, Enter"""

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

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════╗
║     TEST SAVE SEQUENCE: SHIFT+TAB METHOD      ║
╚════════════════════════════════════════════════╝
""")

print(f"Using coordinates: Kinic button at ({config['kinic_x']}, {config['kinic_y']})")
print("\nMake sure you have a webpage open that you want to save!")
input("\nPress Enter when ready...")

print("\n1️⃣  Clicking Kinic button to open extension...")
windows_click(config['kinic_x'], config['kinic_y'])
print("   ✓ Clicked")

print("\n2️⃣  Waiting for Kinic to open...")
time.sleep(2.5)
print("   ✓ Waited 2.5 seconds")

print("\n3️⃣  Pressing Shift+Tab to focus save button...")
send_keys("+{TAB}")
print("   ✓ Sent Shift+Tab")

print("\n4️⃣  Waiting a moment...")
time.sleep(0.8)
print("   ✓ Waited 0.8 seconds")

print("\n5️⃣  Pressing Enter to save...")
send_keys("{ENTER}")
print("   ✓ Sent Enter")

print("\n" + "="*50)
print("✅ SAVE SEQUENCE COMPLETE!")
print("="*50)
print("\nCheck your Kinic - the page should be saved now!")
print("If it worked, the save sequence is correct.")
print("If not, we may need to adjust timing or coordinates.")