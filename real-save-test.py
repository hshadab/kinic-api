#!/usr/bin/env python3
"""Actually save a page to Kinic and verify it worked"""

import subprocess
import time
import requests

def open_url_in_chrome(url):
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
║        REAL KINIC SAVE TEST                   ║
╚════════════════════════════════════════════════╝
""")

# URL to save
url = "https://github.com/python/cpython/blob/main/Lib/random.py"

print(f"1️⃣ Opening URL in Chrome...")
open_url_in_chrome(url)

print("2️⃣ Waiting for page to fully load...")
time.sleep(6)  # Give page time to load

print("3️⃣ Saving to Kinic...")
response = requests.post("http://localhost:5005/save")

if response.json().get('success'):
    print("✅ SAVE SUCCESSFUL!")
    print("\n4️⃣ TO VERIFY:")
    print("   • Click the Kinic extension icon in Chrome")
    print("   • You should see the Python random.py page saved")
    print(f"   • URL: {url}")
else:
    print(f"❌ Save failed: {response.json()}")

print("\n" + "="*50)
print("Check Kinic now to see if it saved!")
print("="*50)