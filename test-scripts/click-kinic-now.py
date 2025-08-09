#!/usr/bin/env python3
"""Direct click test for Kinic"""

import pyautogui
import time
import json
import os

# Disable failsafe
pyautogui.FAILSAFE = False

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("Kinic Direct Click Test")
print("=" * 40)
print(f"Config: {config}")
print(f"\nKinic position: ({config['kinic_x']}, {config['kinic_y']})")

print("\n⚠️  Make sure Chrome with Kinic extension is visible!")
print("Clicking in 3 seconds...")

for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print(f"\nClicking at ({config['kinic_x']}, {config['kinic_y']})...")
pyautogui.click(config['kinic_x'], config['kinic_y'])

print("✅ Click sent!")
print("\nIf Kinic didn't open, the position might be wrong.")
print("The saved position is: x=633, y=413")
print("\nTo reconfigure, delete ~/.kinic/config.json and run again.")