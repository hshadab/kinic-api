#!/bin/bash

echo "🔨 Building Kinic Desktop locally..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install pyinstaller pyautogui pyperclip pillow

# Build the executable
echo "Building executable..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    pyinstaller --name=KinicDesktop \
                --onefile \
                --windowed \
                --add-data="kinic-api.py:." \
                kinic-final.py
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    pyinstaller --name=KinicDesktop \
                --onefile \
                --windowed \
                --add-data="kinic-api.py;." \
                kinic-final.py
else
    # Linux
    pyinstaller --name=KinicDesktop \
                --onefile \
                --add-data="kinic-api.py:." \
                kinic-final.py
fi

echo "✅ Build complete! Executable is in dist/KinicDesktop"
echo "Run it with: ./dist/KinicDesktop"