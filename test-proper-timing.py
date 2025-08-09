#!/usr/bin/env python3
"""Test save with proper 2-second minimum delays"""

import requests
import subprocess
import time
from datetime import datetime

def open_url(url):
    ps_script = f'Start-Process "chrome.exe" -ArgumentList "{url}"'
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def log_time(message):
    """Print with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

print("""
╔════════════════════════════════════════════════╗
║   TESTING SAVE WITH PROPER 2-SECOND DELAYS    ║
╚════════════════════════════════════════════════╝

Total expected time: ~11 seconds
- Focus Chrome: 2s
- Close existing popup: 2s  
- Open Kinic: 3s
- Navigate to save: 2s
- Save: 2s
- Close: instant

Let's test!
""")

# Open a test page
url = "https://realpython.com/python-testing/"
log_time(f"Opening: {url}")
open_url(url)

log_time("Waiting 5 seconds for page to load...")
time.sleep(5)

log_time("Starting save sequence...")
start_time = time.time()

# Call the API
response = requests.post("http://localhost:5006/save", timeout=30)

end_time = time.time()
duration = end_time - start_time

log_time(f"Save completed in {duration:.1f} seconds")

if response.json().get('success'):
    print("\n✅ SUCCESS!")
    print(f"   API Response: {response.json()['message']}")
    print(f"   Duration: {duration:.1f} seconds (expected ~11s)")
    print("\nPlease verify:")
    print("1. Check Kinic for the saved page")
    print("2. Kinic should be closed automatically")
else:
    print(f"\n❌ Failed: {response.json()}")

print("\n" + "="*50)