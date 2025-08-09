#!/usr/bin/env python3
"""Simple test - just save a page"""

import requests
import subprocess
import time
from datetime import datetime

def open_url(url):
    """Open URL in Chrome"""
    ps_script = f'Start-Process "chrome.exe" -ArgumentList "{url}"'
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    print(f"✅ Opened: {url}")

print("""
╔════════════════════════════════════════════════╗
║        SIMPLE SAVE TEST                       ║
╚════════════════════════════════════════════════╝
""")

# URL to test
url = "https://docs.python.org/3/tutorial/index.html"

print(f"Step 1: Opening {url}")
open_url(url)

print("Step 2: Waiting 5 seconds for page to load...")
time.sleep(5)

print("Step 3: Calling save API...")
print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting save...")

try:
    response = requests.post("http://localhost:5006/save", timeout=30)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Save complete!")
    
    if response.json().get('success'):
        print("\n✅ SUCCESS!")
        print(f"Response: {response.json()['message']}")
        print("\nPLEASE CHECK:")
        print("1. Open Kinic extension")
        print(f"2. Look for: {url}")
        print("3. It should be saved")
    else:
        print(f"\n❌ Failed: {response.json()}")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*50)