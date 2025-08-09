#!/usr/bin/env python3
"""Capture exact mouse position using Windows PowerShell"""

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

def main():
    print("=" * 60)
    print("EXACT KINIC POSITION FINDER")
    print("=" * 60)
    print("\nThis will capture the EXACT position of your mouse")
    print("\nInstructions:")
    print("1. Position your mouse EXACTLY on the Kinic button")
    print("2. Don't move it!")
    print("3. Press ENTER here to capture the position")
    print("-" * 60)
    
    input("\nPress ENTER when your mouse is on the Kinic button...")
    
    print("\nCapturing position in 3 seconds (don't move the mouse!)...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Get the exact position
    x, y = get_mouse_position()
    
    if x and y:
        print(f"\n✅ CAPTURED: Kinic button is at ({x}, {y})")
        
        # Update config
        config_file = os.path.expanduser("~/.kinic/config.json")
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        
        config['kinic_x'] = x
        config['kinic_y'] = y
        
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Config updated: {config_file}")
        
        print("\n" + "=" * 60)
        print("TO UPDATE THE API SERVER:")
        print("-" * 60)
        print(f'curl -X POST http://localhost:5003/setup \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"x":{x},"y":{y}}}\'')
        print("=" * 60)
        
        # Automatically update if API is running
        print("\nTrying to update API server...")
        try:
            import requests
            response = requests.post('http://localhost:5003/setup', json={'x': x, 'y': y})
            if response.status_code == 200:
                print("✅ API server updated successfully!")
            else:
                print("⚠️  Could not update API server - run the curl command above")
        except:
            print("⚠️  API server not running - start it and run the curl command above")
    else:
        print("❌ Failed to capture position")

if __name__ == "__main__":
    main()