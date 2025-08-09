#!/usr/bin/env python3
import pyautogui
import time

print("Testing mouse tracking...")
print("Move your mouse around")

for i in range(10):
    x, y = pyautogui.position()
    print(f"Position {i}: ({x}, {y})")
    time.sleep(0.5)

print("Done tracking")