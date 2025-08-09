#!/bin/bash

echo "🚀 Starting Kinic Desktop..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q pyautogui pyperclip pillow

# Run the application
echo "Starting application..."
python3 kinic-final.py