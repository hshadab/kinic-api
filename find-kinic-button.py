#!/usr/bin/env python3
"""Helper to find Kinic button position by testing clicks"""

import pyautogui
import time
import sys

pyautogui.FAILSAFE = False

print("Kinic Button Position Finder")
print("=" * 50)
print("\nThis will help you find the Kinic extension button position.")
print("\nCommon positions for browser extension buttons:")
print("  - Top right area: x=1100-1250, y=50-100")
print("  - Near address bar: x=900-1100, y=50-100")
print("\nMake sure Chrome is open with Kinic extension visible!\n")

def test_click(x, y):
    """Test a single click at position"""
    print(f"\nClicking at ({x}, {y}) in 2 seconds...")
    print("Watch your Chrome browser!")
    time.sleep(2)
    pyautogui.click(x, y)
    print("Clicked! Did Kinic open? (Check Chrome)")
    
def guided_search():
    """Guided search for button"""
    print("\nLet's search systematically...")
    print("I'll click in common extension button areas.")
    print("Watch Chrome and note which click opens Kinic.\n")
    
    # Common positions for extensions (adjust based on screen resolution)
    test_positions = [
        # Top right corner area (common for extensions)
        (1200, 70),
        (1150, 70),
        (1100, 70),
        (1050, 70),
        (1000, 70),
        (950, 70),
        
        # Alternative row
        (1200, 90),
        (1150, 90),
        (1100, 90),
        (1050, 90),
        
        # Your previous position
        (633, 413),
    ]
    
    for i, (x, y) in enumerate(test_positions, 1):
        input(f"\nPress ENTER to test position {i}/{len(test_positions)}: ({x}, {y})")
        pyautogui.click(x, y)
        response = input("Did Kinic open? (y/n/q to quit): ").lower()
        
        if response == 'y':
            print(f"\n✅ Found it! Kinic button is at ({x}, {y})")
            print(f"\nTo save this position, run:")
            print(f'curl -X POST http://localhost:5001/setup/kinic-position -H "Content-Type: application/json" -d \'{{"x":{x},"y":{y}}}\'')
            return x, y
        elif response == 'q':
            break
    
    return None, None

def manual_test():
    """Manual position testing"""
    print("\nManual testing mode")
    print("Enter coordinates to test, or 'q' to quit\n")
    
    while True:
        coords = input("Enter x,y coordinates (e.g., 1100,70): ")
        if coords.lower() == 'q':
            break
            
        try:
            x, y = map(int, coords.split(','))
            test_click(x, y)
            
            response = input("Did Kinic open? (y/n): ").lower()
            if response == 'y':
                print(f"\n✅ Found it! Kinic button is at ({x}, {y})")
                print(f"\nTo save this position, run:")
                print(f'curl -X POST http://localhost:5001/setup/kinic-position -H "Content-Type: application/json" -d \'{{"x":{x},"y":{y}}}\'')
                return x, y
        except:
            print("Invalid format. Use: x,y (e.g., 1100,70)")
    
    return None, None

if __name__ == "__main__":
    print("\nChoose search method:")
    print("1. Guided search (recommended)")
    print("2. Manual coordinate entry")
    print("3. Quick test at common positions")
    
    choice = input("\nEnter choice (1/2/3): ")
    
    if choice == '1':
        guided_search()
    elif choice == '2':
        manual_test()
    elif choice == '3':
        print("\nQuick testing common positions...")
        positions = [(1200,70), (1150,70), (1100,70), (1050,70), (633,413)]
        for x, y in positions:
            input(f"\nPress ENTER to test ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(1)
    else:
        print("Invalid choice")