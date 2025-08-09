#!/bin/bash
# Test common extension button positions

echo "Testing common Kinic extension positions..."
echo "Watch your Chrome browser after each click!"
echo ""

# Test position 1
echo "Test 1: Clicking at (1200, 70)"
python3 -c "import pyautogui; import time; time.sleep(2); pyautogui.click(1200, 70)"
sleep 3

# Test position 2  
echo "Test 2: Clicking at (1100, 70)"
python3 -c "import pyautogui; import time; time.sleep(2); pyautogui.click(1100, 70)"
sleep 3

# Test position 3
echo "Test 3: Clicking at (1050, 70)"
python3 -c "import pyautogui; import time; time.sleep(2); pyautogui.click(1050, 70)"
sleep 3

# Test position 4
echo "Test 4: Clicking at (1000, 70)"
python3 -c "import pyautogui; import time; time.sleep(2); pyautogui.click(1000, 70)"
sleep 3

echo ""
echo "Which click opened Kinic? Note the coordinates above."