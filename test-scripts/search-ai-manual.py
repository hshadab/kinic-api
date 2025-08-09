#!/usr/bin/env python3
"""Manual search and AI extraction with better text selection"""

import subprocess
import time
import json
import sys

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

def click_kinic():
    """Click Kinic button"""
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
    [Win32]::SetCursorPos(959, 98)
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

def get_clipboard():
    """Get clipboard content"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    return result.stdout if result.stdout else None

query = sys.argv[1] if len(sys.argv) > 1 else "legal"

print(f"Searching for '{query}' and extracting AI analysis...")

# Open Kinic
print("1. Opening Kinic...")
click_kinic()
time.sleep(2)

# Search
print("2. Searching...")
for _ in range(4):
    send_keys("{TAB}")
    time.sleep(0.2)

send_keys(query)
send_keys("{ENTER}")

print("3. Waiting for search results...")
time.sleep(3)

# Click AI button
print("4. Clicking AI button...")
for _ in range(5):
    send_keys("{TAB}")
    time.sleep(0.2)
send_keys("{ENTER}")

print("5. Waiting for AI to generate response (10 seconds)...")
time.sleep(10)

# Try Ctrl+A to select all in the AI response area
print("6. Selecting AI response text...")
send_keys("^a")  # Ctrl+A to select all
time.sleep(0.5)

# Copy
print("7. Copying text...")
send_keys("^c")
time.sleep(1)

# Get clipboard
ai_response = get_clipboard()

if ai_response:
    print("\n" + "=" * 60)
    print("AI ANALYSIS:")
    print("-" * 60)
    print(ai_response)
    print("=" * 60)
else:
    print("\n❌ No AI response captured")

# Close Kinic
send_keys("{ESC}")