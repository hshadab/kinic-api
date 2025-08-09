#!/bin/bash

echo "🚀 Starting Kinic Desktop..."

# Kill any existing instances
pkill -f "python.*kinic" 2>/dev/null

# Activate virtual environment and run
cd /home/hshadab/kinic
source venv/bin/activate
python kinic-final.py