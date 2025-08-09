#!/usr/bin/env python3
"""Direct Kinic control test - simplified version"""

import pyautogui
import time
import json
import os

print("Kinic Control Test")
print("=" * 40)

# Disable failsafe
pyautogui.FAILSAFE = False

# Check if config exists
config_file = os.path.expanduser("~/.kinic/config.json")
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"Found existing config: {config}")
    
    if config.get('kinic_x') and config.get('kinic_y'):
        print(f"\nKinic position is set to: ({config['kinic_x']}, {config['kinic_y']})")
        
        response = input("\nDo you want to test clicking at this position? (y/n): ")
        if response.lower() == 'y':
            print("\nMake sure Chrome with Kinic extension is open...")
            time.sleep(2)
            print(f"Clicking at ({config['kinic_x']}, {config['kinic_y']})...")
            pyautogui.click(config['kinic_x'], config['kinic_y'])
            print("Click sent! Check if Kinic opened.")
    else:
        print("Config file exists but no position saved.")
else:
    print("No config file found.")
    
print("\n" + "=" * 40)
print("Setting up new Kinic position...")
print("\nInstructions:")
print("1. Open Chrome browser")
print("2. Make sure the Kinic extension icon is visible")
print("3. Hover your mouse over the Kinic icon (don't click)")
print("4. Note the position and come back here\n")

input("Press ENTER when you're ready and hovering over Kinic icon...")

print("\nRecording position in 3 seconds...")
for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

x, y = pyautogui.position()
print(f"\n✅ Captured position: ({x}, {y})")

# Save config
os.makedirs(os.path.dirname(config_file), exist_ok=True)
config = {'kinic_x': x, 'kinic_y': y}
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
print(f"Saved to {config_file}")

# Test the click
test = input("\nDo you want to test clicking at this position? (y/n): ")
if test.lower() == 'y':
    print(f"\nClicking at ({x}, {y}) in 2 seconds...")
    time.sleep(2)
    pyautogui.click(x, y)
    print("Click sent! Check if Kinic opened.")

print("\n✅ Setup complete!")
print("\nYou can now use any of the kinic Python files:")
print("  - kinic-working.py (full GUI version)")
print("  - kinic-final.py (simpler GUI)")
print("  - kinic-api.py (API server)")