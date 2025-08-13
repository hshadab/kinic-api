#!/usr/bin/env python3
"""Capture AI response position - Windows native version"""

import time
import json
import pyautogui
import os

print("\n" + "="*60)
print("CAPTURE AI RESPONSE POSITION")
print("="*60)

print("\nINSTRUCTIONS:")
print("1. Open Chrome with Kinic extension")
print("2. Click Kinic button")
print("3. Search for something (e.g., 'test')")
print("4. Click the AI button to generate response")
print("5. Wait for AI text to appear")
print("6. Position mouse IN THE CENTER of the AI response text")
print("\nPress ENTER when ready...")
input()

print("\nCapturing in 3 seconds...")
for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Get mouse position
x, y = pyautogui.position()

print(f"\n✅ Captured AI response position: ({x}, {y})")

# Load existing config or create new
if os.path.exists('kinic-config.json'):
    with open('kinic-config.json', 'r') as f:
        config = json.load(f)
else:
    config = {}

# Update AI response coordinates
config['ai_response_x'] = x
config['ai_response_y'] = y

# Save config
with open('kinic-config.json', 'w') as f:
    json.dump(config, f, indent=4)

print(f"✅ Saved to kinic-config.json")
print("\nConfiguration complete! You can now run:")
print("  python kinic-api-robust.py")