#!/usr/bin/env python3
"""Find exact Kinic button position by testing nearby coordinates"""

import subprocess
import time

def windows_click(x, y):
    """Click at position using Windows PowerShell"""
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
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

print("Kinic Button Position Finder")
print("=" * 50)
print("\nTesting positions around (904, 96)...")
print("Watch Chrome to see which click opens Kinic\n")

# Test in a grid around the expected position
base_x, base_y = 904, 96
positions = []

# Create a grid of test positions
for x_offset in [-10, -5, 0, 5, 10]:
    for y_offset in [-5, 0, 5]:
        positions.append((base_x + x_offset, base_y + y_offset))

print(f"Will test {len(positions)} positions:")
for i, (x, y) in enumerate(positions, 1):
    print(f"\n[{i}/{len(positions)}] Testing ({x}, {y})...")
    windows_click(x, y)
    time.sleep(2)  # Wait to see if Kinic opens
    
    if i % 5 == 0:
        response = input("Did any of the last 5 clicks open Kinic? (y/n): ")
        if response.lower() == 'y':
            print("\nLast 5 positions were:")
            for j in range(max(0, i-5), i):
                print(f"  {j+1}. {positions[j]}")
            choice = input("Which number opened Kinic? ")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(positions):
                    x, y = positions[idx]
                    print(f"\n✅ Found it! Kinic button is at ({x}, {y})")
                    print(f"\nUpdate with:")
                    print(f'curl -X POST http://localhost:5002/setup/kinic -H "Content-Type: application/json" -d \'{{"x":{x},"y":{y}}}\'')
                    exit(0)
            except:
                pass

print("\nIf none worked, try running your mouse coordinate tool again to get exact position.")