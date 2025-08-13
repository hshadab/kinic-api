#!/usr/bin/env python3

import pyautogui
import time

print("Testing pyautogui mouse control...")
print("Current mouse position:", pyautogui.position())

try:
    print("Attempting to move mouse...")
    pyautogui.moveTo(100, 100)
    time.sleep(1)
    print("New mouse position:", pyautogui.position())
    
    print("Attempting to click...")
    pyautogui.click(200, 200)
    print("Click completed")
    
except Exception as e:
    print(f"Error: {e}")
    print("pyautogui cannot control mouse from WSL -> Windows")