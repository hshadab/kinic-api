#!/usr/bin/env python3
"""Test if pyautogui mouse movement works"""

import sys
import time

try:
    import pyautogui
    print("✅ pyautogui imported successfully")
    
    # Disable failsafe
    pyautogui.FAILSAFE = False
    
    # Get current position
    current = pyautogui.position()
    print(f"Current mouse position: {current}")
    
    # Try to move mouse
    print("Moving mouse by 100 pixels right and down...")
    pyautogui.moveTo(current.x + 100, current.y + 100, duration=1.0)
    
    new_pos = pyautogui.position()
    print(f"New mouse position: {new_pos}")
    
    # Move back
    print("Moving back to original position...")
    pyautogui.moveTo(current.x, current.y, duration=1.0)
    
    print("✅ Mouse movement test successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()