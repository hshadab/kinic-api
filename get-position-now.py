#!/usr/bin/env python3
"""Get exact mouse position RIGHT NOW"""

import subprocess
import time

print("POSITION CAPTURE - Move your mouse to Kinic button NOW!")
print("=" * 50)
print("Capturing position in 5 seconds...")

for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

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
    print(f"\n✅ CAPTURED: Mouse is at ({x}, {y})")
    print(f"\nUpdate with:")
    print(f'curl -X POST http://localhost:5003/setup -H "Content-Type: application/json" -d \'{{"x":{x},"y":{y}}}\'')
else:
    print("Failed to get position")