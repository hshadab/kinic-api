#!/usr/bin/env python3
"""Reconfigure Kinic position"""

import pyautogui
import time
import json
import os

# Disable failsafe
pyautogui.FAILSAFE = False

print("Kinic Position Reconfiguration")
print("=" * 40)

config_file = os.path.expanduser("~/.kinic/config.json")

print("\nCurrent mouse tracking test:")
print("Move your mouse around and watch the coordinates update...")
print("Press Ctrl+C when you've found the Kinic icon position\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})    ", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nPosition tracking stopped.")
    
    x, y = pyautogui.position()
    print(f"\nLast position: ({x}, {y})")
    
    # Save new config
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    config = {'kinic_x': x, 'kinic_y': y}
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Saved new position to {config_file}")
    print("\nTesting click in 2 seconds...")
    time.sleep(2)
    
    pyautogui.click(x, y)
    print("Click sent! Check if Kinic opened.")