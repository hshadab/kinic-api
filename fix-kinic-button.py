#!/usr/bin/env python3
"""
Fix Kinic button position - Quick recapture
"""

import time
import json
import pyautogui

print("\n" + "="*60)
print("FIX KINIC BUTTON POSITION")
print("="*60)

# Load current config to show what's wrong
try:
    with open('kinic-config.json', 'r') as f:
        config = json.load(f)
    print(f"\n❌ Current (wrong) position: ({config['kinic_x']}, {config['kinic_y']})")
except:
    config = {}
    print("\n⚠️ No config file found")

print("\n📍 To capture the CORRECT position:")
print("  1. Make sure Chrome is open")
print("  2. Make sure Kinic extension is visible")
print("  3. Position your mouse EXACTLY on the Kinic button")
print("  4. Press Enter and DON'T MOVE for 5 seconds")

input("\n✋ Position mouse on Kinic button and press Enter...")

print("\nCapturing in...")
for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Get mouse position
x, y = pyautogui.position()

print(f"\n✅ NEW Kinic button position: ({x}, {y})")

# Update config
config['kinic_x'] = x
config['kinic_y'] = y

# Save
with open('kinic-config.json', 'w') as f:
    json.dump(config, f, indent=4)

print("\n✅ Saved to kinic-config.json")
print("\n⚠️ RESTART the API for changes to take effect:")
print("  1. Stop API with Ctrl+C")
print("  2. Run: python kinic-api.py")