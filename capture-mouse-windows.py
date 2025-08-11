#!/usr/bin/env python3
"""Capture mouse position - Windows native version"""

import time
import json
import pyautogui

print("\n" + "="*60)
print("CAPTURING MOUSE POSITION IN 3 SECONDS")
print("="*60)
print("\n⚠️  POSITION YOUR MOUSE ON THE KINIC BUTTON!")
print("\nCapturing in...")

for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Get mouse position using pyautogui
x, y = pyautogui.position()

print(f"\n✅ Captured position: ({x}, {y})")

# Update config
config = {
    'kinic_x': x,
    'kinic_y': y,
    'ai_response_x': 1011,  # Keep existing or update later
    'ai_response_y': 815    # Keep existing or update later
}

# Save to file
with open('kinic-config.json', 'w') as f:
    json.dump(config, f, indent=4)

print(f"✅ Saved to kinic-config.json")
print("\nNow run this to capture AI response position:")
print("  python capture-ai-windows.py")