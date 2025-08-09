#!/usr/bin/env python3
"""Direct test without GUI"""

import os
os.environ['DISPLAY'] = ':0'

import pyautogui
import time

print("Testing mouse movement directly...")

# Disable failsafe
pyautogui.FAILSAFE = False

# Get screen size
width, height = pyautogui.size()
print(f"Screen size: {width}x{height}")

# Get current position
x, y = pyautogui.position()
print(f"Current position: ({x}, {y})")

# Move mouse
print("Moving mouse to center of screen...")
pyautogui.moveTo(width/2, height/2, duration=1)

time.sleep(1)

print("Moving to top-left...")
pyautogui.moveTo(100, 100, duration=1)

time.sleep(1)

print("Moving back to original position...")
pyautogui.moveTo(x, y, duration=1)

print("Done!")