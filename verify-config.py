#!/usr/bin/env python3
"""
Verify Kinic configuration and test mouse positioning
"""

import json
import os
import pyautogui
import time

print("\n" + "="*60)
print("KINIC CONFIGURATION VERIFICATION")
print("="*60)

# Check config file
config_file = "kinic-config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"\n✅ Config file found: {config_file}")
else:
    print(f"\n❌ Config file not found!")
    print("Please run: python capture-mouse-windows.py")
    exit(1)

# Display current configuration
print("\n📋 Current Configuration:")
print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
print(f"  AI response:  ({config['ai_response_x']}, {config['ai_response_y']})")

# Test mouse movement
print("\n🖱️ Testing mouse positioning...")
print("\nThis will move your mouse to each configured position.")
input("Press Enter to start the test...")

# Test Kinic button position
print(f"\n1. Moving to Kinic button position ({config['kinic_x']}, {config['kinic_y']})...")
pyautogui.moveTo(config['kinic_x'], config['kinic_y'], duration=1)
time.sleep(2)
response = input("   Is the mouse on the Kinic extension button? (y/n): ")

if response.lower() != 'y':
    print("\n⚠️ Kinic button position needs updating!")
    print("Run: python capture-mouse-windows.py")
else:
    print("   ✅ Kinic button position is correct")

# Test AI response position
print(f"\n2. Moving to AI response position ({config['ai_response_x']}, {config['ai_response_y']})...")
pyautogui.moveTo(config['ai_response_x'], config['ai_response_y'], duration=1)
time.sleep(2)
response = input("   Is the mouse in the AI response text area? (y/n): ")

if response.lower() != 'y':
    print("\n⚠️ AI response position needs updating!")
    print("Run: python capture-ai-windows.py")
else:
    print("   ✅ AI response position is correct")

# Summary
print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)

# Check if API is using same config
print("\n📡 Checking API configuration...")
print("The API will load from: kinic-config.json")
print("Make sure the API is using these coordinates:")
print(f"  Kinic: ({config['kinic_x']}, {config['kinic_y']})")
print(f"  AI:    ({config['ai_response_x']}, {config['ai_response_y']})")

print("\n✅ If positions are correct, you can run:")
print("  1. python kinic-api.py")
print("  2. python test-ai-extraction.py")
print("\n❌ If positions are wrong, update them with:")
print("  • python capture-mouse-windows.py (for Kinic button)")
print("  • python capture-ai-windows.py (for AI response area)")