#!/usr/bin/env python3
"""Reliable Kinic clicker that handles near misses"""

import subprocess
import time
import json
import os

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

def windows_click(x, y):
    """Single click at exact position"""
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

def reliable_kinic_click():
    """Click Kinic with multiple attempts in a small area"""
    base_x = config.get('kinic_x', 962)
    base_y = config.get('kinic_y', 98)
    
    print(f"Attempting to click Kinic around ({base_x}, {base_y})...")
    
    # Try center first
    print(f"  Try 1: Center ({base_x}, {base_y})")
    windows_click(base_x, base_y)
    time.sleep(0.5)
    
    # If that doesn't work, try a small cross pattern
    offsets = [
        (-2, 0),  # left
        (2, 0),   # right
        (0, -2),  # up
        (0, 2),   # down
    ]
    
    for i, (dx, dy) in enumerate(offsets, 2):
        x, y = base_x + dx, base_y + dy
        print(f"  Try {i}: ({x}, {y})")
        windows_click(x, y)
        time.sleep(0.5)

def find_working_position():
    """Interactive mode to find the exact working position"""
    base_x = config.get('kinic_x', 962)
    base_y = config.get('kinic_y', 98)
    
    print(f"\nTesting positions around ({base_x}, {base_y})")
    print("Watch Chrome to see which click opens Kinic\n")
    
    # Test in a grid
    positions = []
    for x in range(-4, 5, 2):  # -4, -2, 0, 2, 4
        for y in range(-4, 5, 2):
            positions.append((base_x + x, base_y + y))
    
    for i, (x, y) in enumerate(positions, 1):
        print(f"Testing position {i}/25: ({x}, {y})")
        windows_click(x, y)
        time.sleep(1.5)
        
        if i % 5 == 0:
            response = input("Did any of the last 5 work? (y/n/skip): ")
            if response.lower() == 'y':
                last_five = positions[max(0, i-5):i]
                print("\nLast 5 positions:")
                for j, pos in enumerate(last_five, i-4):
                    print(f"  {j}: {pos}")
                
                choice = input("Which number worked? ")
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(positions):
                        new_x, new_y = positions[idx]
                        print(f"\n✅ Found working position: ({new_x}, {new_y})")
                        
                        # Update config
                        config['kinic_x'] = new_x
                        config['kinic_y'] = new_y
                        with open(config_file, 'w') as f:
                            json.dump(config, f, indent=2)
                        
                        print("Config updated!")
                        return new_x, new_y
                except:
                    pass

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "find":
        find_working_position()
    else:
        reliable_kinic_click()