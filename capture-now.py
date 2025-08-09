#!/usr/bin/env python3
"""Capture mouse position RIGHT NOW"""

import subprocess
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

print("CAPTURING MOUSE POSITION NOW!")

x, y = get_mouse_position()

if x and y:
    print(f"\n✅ CAPTURED: ({x}, {y})")
    
    # Load existing config
    config_file = os.path.expanduser("~/.kinic/config.json")
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Update AI response position
    config['ai_response_x'] = x
    config['ai_response_y'] = y
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Saved AI response position to config")
    print(f"\nUpdated coordinates:")
    print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
    print(f"  AI response:  ({x}, {y})")
    
    # Also update the API
    print("\n📡 Updating API...")
    import requests
    response = requests.post(
        "http://localhost:5006/setup-ai",
        json={"x": x, "y": y}
    )
    if response.json().get('success'):
        print("✅ API updated with new AI position!")
else:
    print("❌ Failed to capture position")