#!/usr/bin/env python3
"""Capture the position of AI response text area in Kinic"""

import subprocess
import time
import json
import os

def send_keys(keys):
    """Send keyboard keys using PowerShell"""
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def click_kinic():
    """Click Kinic button"""
    config_file = os.path.expanduser("~/.kinic/config.json")
    with open(config_file, 'r') as f:
        config = json.load(f)
    
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
    [Win32]::SetCursorPos({config['kinic_x']}, {config['kinic_y']})
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

def get_mouse_position():
    """Get current mouse position using Windows PowerShell"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    $pos = [System.Windows.Forms.Cursor]::Position
    Write-Output "$($pos.X),$($pos.Y)"
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    if result.stdout:
        x, y = map(int, result.stdout.strip().split(','))
        return x, y
    return None, None

print("=" * 60)
print("AI RESPONSE POSITION CAPTURE")
print("=" * 60)
print("\nThis will help you find where the AI response text appears")
print("\nSetup steps:")
print("1. I'll open Kinic and do a test search")
print("2. I'll click the AI button")
print("3. When the AI response appears, position your mouse on the text")
print("4. I'll capture that position")
print("-" * 60)

print("\nStep 1: Opening Kinic...")
click_kinic()
time.sleep(2)

print("Step 2: Searching for 'test'...")
# Tab to search
for _ in range(4):
    send_keys("{TAB}")
    time.sleep(0.2)

send_keys("test")
send_keys("{ENTER}")

print("Step 3: Waiting for search results...")
time.sleep(3)

print("Step 4: Clicking AI button...")
# Tab to AI button (usually 5 more tabs after search)
for _ in range(5):
    send_keys("{TAB}")
    time.sleep(0.2)
send_keys("{ENTER}")

print("\n" + "=" * 60)
print("⚠️  AI IS GENERATING RESPONSE...")
print("=" * 60)
print("\nWhen you see the AI response text:")
print("1. Position your mouse OVER THE AI RESPONSE TEXT")
print("2. Keep it there during the countdown")
print("\nStarting countdown in 5 seconds (wait for AI to respond)...")
time.sleep(5)

print("\n🎯 POSITION YOUR MOUSE ON THE AI RESPONSE TEXT NOW!")
print("Capturing in 10 seconds...")

for i in range(10, 0, -1):
    print(f"  {i}...", end='\r')
    time.sleep(1)

print("\n\n📸 CAPTURING POSITION!")

# Get position
x, y = get_mouse_position()

if x and y:
    print(f"\n✅ AI Response position captured: ({x}, {y})")
    
    # Update config
    config_file = os.path.expanduser("~/.kinic/config.json")
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    config['ai_response_x'] = x
    config['ai_response_y'] = y
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Config updated with AI response position")
    
    print("\n" + "=" * 60)
    print("UPDATE API SERVER:")
    print("-" * 60)
    print(f'curl -X POST http://localhost:5004/setup-ai \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -d \'{{"x":{x},"y":{y}}}\'')
    print("=" * 60)
else:
    print("❌ Failed to capture position")

# Close Kinic
send_keys("{ESC}")
print("\nKinic closed.")