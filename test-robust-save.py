#!/usr/bin/env python3
"""Test the robust save API"""

import requests
import subprocess
import time

# Open a test page
def open_url(url):
    ps_script = f'Start-Process "chrome.exe" -ArgumentList "{url}"'
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

print("""
╔════════════════════════════════════════════════╗
║     TESTING ROBUST SAVE API                   ║
╚════════════════════════════════════════════════╝

This test will:
✅ Focus Chrome
✅ Close any existing Kinic popup
✅ Save the page
✅ Close Kinic when done
""")

# Open a page to save
url = "https://www.python.org/about/"
print(f"\n1️⃣ Opening test page: {url}")
open_url(url)

print("2️⃣ Waiting 5 seconds for page to load...")
time.sleep(5)

print("3️⃣ Calling robust save API...")
response = requests.post("http://localhost:5006/save")

if response.json().get('success'):
    print("✅ SAVE API RETURNED SUCCESS!")
    print("\n" + "="*50)
    print("VERIFY THE SAVE:")
    print("="*50)
    print("1. Click the Kinic icon in Chrome")
    print(f"2. Look for: {url}")
    print("3. It should be in your saved items")
    print("\nNote: Kinic should have closed automatically!")
else:
    print(f"❌ Save failed: {response.json()}")

print("\n" + "="*50)