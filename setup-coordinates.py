#!/usr/bin/env python3
"""Simple interactive coordinate setup for Kinic"""

import subprocess
import time
import json
import os

def get_mouse_position():
    """Get current mouse position"""
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

def save_config(kinic_x, kinic_y, ai_x, ai_y):
    """Save configuration"""
    config_file = os.path.expanduser("~/.kinic/config.json")
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    
    config = {
        'kinic_x': kinic_x,
        'kinic_y': kinic_y,
        'ai_response_x': ai_x,
        'ai_response_y': ai_y
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_file

print("""
╔══════════════════════════════════════════════════╗
║         KINIC COORDINATE SETUP - SIMPLE         ║
╚══════════════════════════════════════════════════╝

We need to capture 2 positions:
1. Kinic extension button in Chrome
2. AI response text area (when Kinic is open)

Let's start!
""")

# Step 1: Kinic Button
print("\n" + "="*50)
print("STEP 1: KINIC BUTTON POSITION")
print("="*50)
print("\n1. Open Chrome")
print("2. Make sure you can see the Kinic extension icon")
print("3. Hover your mouse over the Kinic icon")
print("4. DON'T CLICK - just hover")

input("\nPress Enter when your mouse is hovering over the Kinic icon...")

kinic_x, kinic_y = get_mouse_position()
print(f"✅ Captured Kinic button: ({kinic_x}, {kinic_y})")

# Step 2: AI Response Area
print("\n" + "="*50)
print("STEP 2: AI RESPONSE AREA")
print("="*50)
print("\n1. Click the Kinic icon to open it")
print("2. Do a search for any term")
print("3. Click the 'AI' button to generate a response")
print("4. Wait for the AI response to appear")
print("5. Position your mouse in the middle of the AI response text")
print("6. DON'T CLICK - just position")

input("\nPress Enter when your mouse is over the AI response text...")

ai_x, ai_y = get_mouse_position()
print(f"✅ Captured AI response area: ({ai_x}, {ai_y})")

# Save configuration
config_file = save_config(kinic_x, kinic_y, ai_x, ai_y)

print("\n" + "="*50)
print("✅ SETUP COMPLETE!")
print("="*50)
print(f"\nConfiguration saved to: {config_file}")
print("\nYour coordinates:")
print(f"  Kinic button: ({kinic_x}, {kinic_y})")
print(f"  AI response:  ({ai_x}, {ai_y})")

print("\nYou can now run the demo:")
print("  python simple-multi-agent.py")
print("\n" + "="*50)