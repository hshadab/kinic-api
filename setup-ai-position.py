#!/usr/bin/env python3
"""Setup AI response position - updates config with current mouse position"""

import subprocess
import json
import os
import time

def get_mouse_position():
    """Get current mouse position"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        using System.Drawing;
        
        public class MouseInfo {
            [DllImport("user32.dll")]
            public static extern bool GetCursorPos(out POINT lpPoint);
            
            [StructLayout(LayoutKind.Sequential)]
            public struct POINT {
                public int X;
                public int Y;
            }
            
            public static string GetPosition() {
                POINT point;
                GetCursorPos(out point);
                return point.X + "," + point.Y;
            }
        }
'@
    [MouseInfo]::GetPosition()
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    if result.stdout:
        coords = result.stdout.strip().split(',')
        return int(coords[0]), int(coords[1])
    return None, None

def save_config(config):
    """Save configuration"""
    config_file = os.path.expanduser("~/.kinic/config.json")
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def load_config():
    """Load existing configuration"""
    config_file = os.path.expanduser("~/.kinic/config.json")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {
        'kinic_x': 1379,
        'kinic_y': 101,
        'ai_response_x': 1000,
        'ai_response_y': 828
    }

print("""
╔════════════════════════════════════════════════════════════╗
║     SETUP AI RESPONSE POSITION                            ║
╠════════════════════════════════════════════════════════════╣
║  1. Make sure Kinic is open with an AI response visible   ║
║  2. Position your mouse on the AI response text area      ║
║  3. This script will capture that position                ║
╚════════════════════════════════════════════════════════════╝
""")

# Load current config
config = load_config()

print("Current configuration:")
print(f"  Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
print(f"  AI response:  ({config.get('ai_response_x')}, {config.get('ai_response_y')})")

print("\n" + "="*60)
print("INSTRUCTIONS:")
print("="*60)
print("""
1. Open Chrome and click the Kinic extension
2. Search for something (e.g., "Python")
3. Click the AI button to generate a response
4. Wait for the AI response to appear
5. Position your mouse cursor IN THE MIDDLE of the AI response text
6. Come back to this terminal and press Enter
""")

input("\nPress Enter when your mouse is positioned on the AI response text...")

print("\nCapturing mouse position in 3 seconds...")
print("Keep your mouse on the AI response text!")
for i in range(3, 0, -1):
    print(f"  {i}...", end='\r')
    time.sleep(1)

# Capture position
x, y = get_mouse_position()

if x and y:
    print(f"\n✅ Captured position: ({x}, {y})")
    
    # Update config
    old_x = config.get('ai_response_x')
    old_y = config.get('ai_response_y')
    
    config['ai_response_x'] = x
    config['ai_response_y'] = y
    
    # Save config
    save_config(config)
    
    print("\n" + "="*60)
    print("CONFIGURATION UPDATED:")
    print("="*60)
    print(f"  Old AI position: ({old_x}, {old_y})")
    print(f"  New AI position: ({x}, {y})")
    print("\n✅ Configuration saved to ~/.kinic/config.json")
    
    print("\nNext steps:")
    print("1. Restart the API server if it's running")
    print("2. Test AI extraction with: python test-ai-extraction.py")
    print("3. Or run the full demo: python multi-agent-demo-auto.py")
else:
    print("\n❌ Failed to capture mouse position")
    print("Please try again")