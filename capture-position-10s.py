#!/usr/bin/env python3
"""Get mouse position with 10 second countdown"""

import subprocess
import time

print("=" * 60)
print("KINIC BUTTON POSITION CAPTURE")
print("=" * 60)
print("\n⚠️  IMPORTANT: Move your mouse to the Kinic button!")
print("\nYou have 10 seconds to position your mouse...")
print("-" * 60)

for i in range(10, 0, -1):
    print(f"Capturing in {i} seconds... (move mouse to Kinic button!)", end='\r')
    time.sleep(1)

print("\n\n🎯 CAPTURING NOW!")

# Get position using Windows PowerShell
ps_script = """
Add-Type -AssemblyName System.Windows.Forms
$pos = [System.Windows.Forms.Cursor]::Position
Write-Output "$($pos.X),$($pos.Y)"
"""

result = subprocess.run(
    ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
     "-ExecutionPolicy", "Bypass", "-Command", ps_script],
    capture_output=True, text=True
)

if result.stdout:
    x, y = map(int, result.stdout.strip().split(','))
    print(f"\n✅ CAPTURED: Position is ({x}, {y})")
    print("\n" + "=" * 60)
    print("UPDATE YOUR CONFIG:")
    print("-" * 60)
    print(f'curl -X POST http://localhost:5003/setup \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -d \'{{"x":{x},"y":{y}}}\'')
    print("=" * 60)
else:
    print("❌ Failed to get position")