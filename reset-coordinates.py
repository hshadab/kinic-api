#!/usr/bin/env python3
"""Reset both Kinic button and AI response coordinates"""

import subprocess
import time
import json
import os

def get_mouse_position():
    """Get current mouse position using Windows PowerShell"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    $pos = [System.Windows.Forms.Cursor]::Position
    Write-Output "$($pos.X),$($pos.Y)"
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    if result.stdout:
        x, y = map(int, result.stdout.strip().split(','))
        return x, y
    return None, None

print("=" * 60)
print("COORDINATE RESET TOOL")
print("=" * 60)
print("\nWe'll capture 2 positions:")
print("1. Kinic extension button")
print("2. AI response text area")
print("-" * 60)

config_file = os.path.expanduser("~/.kinic/config.json")
config = {}

# Capture Kinic button position
print("\n📍 STEP 1: KINIC BUTTON POSITION")
print("-" * 40)
print("Position your mouse on the Kinic extension button in Chrome")
print("You have 10 seconds...")

for i in range(10, 0, -1):
    print(f"  {i}...", end='\r')
    time.sleep(1)

print("\n📸 Capturing Kinic button position...")
kinic_x, kinic_y = get_mouse_position()

if kinic_x and kinic_y:
    print(f"✅ Kinic button: ({kinic_x}, {kinic_y})")
    config['kinic_x'] = kinic_x
    config['kinic_y'] = kinic_y
else:
    print("❌ Failed to capture Kinic position")
    exit(1)

# Capture AI response position
print("\n📍 STEP 2: AI RESPONSE TEXT POSITION")
print("-" * 40)
print("For this step, you need to:")
print("1. Open Kinic manually")
print("2. Do a search")
print("3. Click the AI button")
print("4. When AI response appears, position mouse on the text")
print("\nYou have 20 seconds to do this...")

for i in range(20, 0, -1):
    print(f"  {i}...", end='\r')
    time.sleep(1)

print("\n📸 Capturing AI response position...")
ai_x, ai_y = get_mouse_position()

if ai_x and ai_y:
    print(f"✅ AI response text: ({ai_x}, {ai_y})")
    config['ai_response_x'] = ai_x
    config['ai_response_y'] = ai_y
else:
    print("⚠️  No AI response position captured - using default")
    config['ai_response_x'] = 600
    config['ai_response_y'] = 400

# Save config
os.makedirs(os.path.dirname(config_file), exist_ok=True)
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("\n" + "=" * 60)
print("✅ CONFIGURATION SAVED")
print("-" * 60)
print(f"Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
print(f"AI response: ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
print("\n" + "=" * 60)
print("UPDATE API SERVER WITH THESE COMMANDS:")
print("-" * 60)
print(f"# Update Kinic button position:")
print(f"curl -X POST http://localhost:5005/setup-kinic \\")
print(f"  -H \"Content-Type: application/json\" \\")
print(f"  -d '{{\"x\":{config['kinic_x']},\"y\":{config['kinic_y']}}}'")
print()
print(f"# Update AI response position:")
print(f"curl -X POST http://localhost:5005/setup-ai \\")
print(f"  -H \"Content-Type: application/json\" \\")
print(f"  -d '{{\"x\":{config.get('ai_response_x')},\"y\":{config.get('ai_response_y')}}}'")
print("=" * 60)