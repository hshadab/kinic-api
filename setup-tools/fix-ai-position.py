#!/usr/bin/env python3
"""
Fix AI response text position - Quick recapture
"""

import time
import json
import pyautogui

print("\n" + "="*60)
print("FIX AI RESPONSE POSITION")
print("="*60)

# Load current config to show what's wrong
try:
    with open('kinic-config.json', 'r') as f:
        config = json.load(f)
    print(f"\n❌ Current (wrong) AI position: ({config['ai_response_x']}, {config['ai_response_y']})")
except:
    config = {}
    print("\n⚠️ No config file found")

print("\n📍 To capture the CORRECT position:")
print("  1. Open Chrome with Kinic")
print("  2. Click Kinic button")
print("  3. Search for something (e.g., 'test')")
print("  4. Click the AI button")
print("  5. WAIT for AI text to appear")
print("  6. Position mouse in CENTER of the AI response text")
print("  7. Press Enter and DON'T MOVE for 5 seconds")

input("\n✋ Position mouse in CENTER of AI text and press Enter...")

print("\nCapturing in...")
for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Get mouse position
x, y = pyautogui.position()

print(f"\n✅ NEW AI response position: ({x}, {y})")

# Update config
config['ai_response_x'] = x
config['ai_response_y'] = y

# Save
with open('kinic-config.json', 'w') as f:
    json.dump(config, f, indent=4)

print("\n✅ Saved to kinic-config.json")
print("\n⚠️ RESTART the API for changes to take effect:")
print("  1. Stop API with Ctrl+C")
print("  2. Run: python kinic-api.py")