#!/usr/bin/env python3
"""
Quick fix for Kinic button position
"""

import time
import json
import pyautogui

print("\n" + "="*60)
print("QUICK FIX - CAPTURE KINIC BUTTON POSITION")
print("="*60)

print("\n⚠️  IMPORTANT:")
print("1. Make sure Chrome is open")
print("2. Make sure Kinic extension is visible in toolbar")
print("3. Position your mouse EXACTLY on the Kinic button")
print("\nYou have 5 seconds after pressing Enter...")

input("\nPress Enter when ready...")

print("\nCapturing in...")
for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Get mouse position
x, y = pyautogui.position()

print(f"\n✅ Captured NEW Kinic position: ({x}, {y})")

# Load existing config
try:
    with open('kinic-config.json', 'r') as f:
        config = json.load(f)
    print(f"❌ OLD Kinic position was: ({config['kinic_x']}, {config['kinic_y']})")
except:
    config = {}

# Update only Kinic button coordinates
config['kinic_x'] = x
config['kinic_y'] = y

# Keep AI response coordinates
if 'ai_response_x' not in config:
    config['ai_response_x'] = 1413
if 'ai_response_y' not in config:
    config['ai_response_y'] = 1244

# Save config
with open('kinic-config.json', 'w') as f:
    json.dump(config, f, indent=4)

print(f"\n✅ Config updated!")
print(f"\nNew configuration:")
print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
print(f"  AI response:  ({config['ai_response_x']}, {config['ai_response_y']})")

print(f"\n⚠️  RESTART THE API to use new coordinates:")
print(f"  1. Stop the API (Ctrl+C)")
print(f"  2. Run: python kinic-api.py")
print(f"\nThe API will load the new coordinates from kinic-config.json")