#!/usr/bin/env python3
"""Simple Kinic clicker - just clicks at saved position"""

import pyautogui
import time
import sys

# Disable failsafe
pyautogui.FAILSAFE = False

# Known Kinic position (from your config)
KINIC_X = 633
KINIC_Y = 413

def click_kinic():
    """Click the Kinic icon"""
    print(f"Clicking Kinic at ({KINIC_X}, {KINIC_Y})...")
    pyautogui.click(KINIC_X, KINIC_Y)
    print("✅ Clicked!")
    
def save_page():
    """Save current page to Kinic"""
    click_kinic()
    time.sleep(2)  # Wait for Kinic to open
    pyautogui.hotkey('shift', 'tab')
    time.sleep(0.5)
    pyautogui.press('enter')
    print("✅ Save command sent!")

def search_kinic(query):
    """Search in Kinic"""
    click_kinic()
    time.sleep(2)  # Wait for Kinic to open
    
    # Tab to search field (4 times)
    for _ in range(4):
        pyautogui.press('tab')
        time.sleep(0.2)
    
    pyautogui.typewrite(query)
    pyautogui.press('enter')
    print(f"✅ Searched for: {query}")

if __name__ == "__main__":
    print("Kinic Controller")
    print("=" * 40)
    print("Commands:")
    print("  1. click   - Click Kinic icon")
    print("  2. save    - Save current page")
    print("  3. search <query> - Search in Kinic")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python kinic-click-api.py [click|save|search <query>]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "click":
        click_kinic()
    elif command == "save":
        save_page()
    elif command == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        search_kinic(query)
    else:
        print("Invalid command")
        print("Usage: python kinic-click-api.py [click|save|search <query>]")