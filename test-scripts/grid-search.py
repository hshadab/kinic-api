#!/usr/bin/env python3
"""Grid search to find Kinic button"""

import pyautogui
import time

pyautogui.FAILSAFE = False

print("Kinic Button Grid Search")
print("=" * 50)
print("\nI'll click in a grid pattern across the top of your screen.")
print("Watch for when Kinic opens and note the position.\n")

# Search in the top area where extensions usually are
# Screen is 1280x800, so search the top right area

positions = []
# Search top right area (where extensions typically are)
for x in range(900, 1280, 50):  # From x=900 to 1280 in steps of 50
    for y in range(50, 120, 20):  # From y=50 to 120 in steps of 20
        positions.append((x, y))

print(f"Will test {len(positions)} positions in the top toolbar area...")
print("Each click will be 2 seconds apart.\n")

for i, (x, y) in enumerate(positions, 1):
    print(f"[{i}/{len(positions)}] Clicking at ({x}, {y})...")
    pyautogui.click(x, y)
    time.sleep(2)
    
    # Check every 5 clicks
    if i % 5 == 0:
        response = input("Did Kinic open in any of the last 5 clicks? (y/n/q to quit): ").lower()
        if response == 'y':
            last_five = positions[max(0, i-5):i]
            print("\nLast 5 positions were:")
            for j, (px, py) in enumerate(last_five, i-4):
                print(f"  {j}. ({px}, {py})")
            
            which = input("Which number opened Kinic? ")
            try:
                idx = int(which) - 1
                if 0 <= idx < len(positions):
                    fx, fy = positions[idx]
                    print(f"\n✅ Found it! Kinic is at ({fx}, {fy})")
                    print(f"\nSet it with:")
                    print(f'curl -X POST http://localhost:5001/setup/kinic-position -H "Content-Type: application/json" -d \'{{"x":{fx},"y":{fy}}}\'')
                    break
            except:
                pass
        elif response == 'q':
            break

print("\nSearch complete!")