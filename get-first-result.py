#!/usr/bin/env python3
"""Get the first search result from Kinic"""

import subprocess
import time
import pyperclip

def send_keys(keys):
    """Send keyboard keys using PowerShell"""
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def copy_to_clipboard():
    """Copy selected text using Ctrl+C"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("^c")
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def get_clipboard():
    """Get clipboard content using PowerShell"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    """
    
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    
    return result.stdout.strip() if result.stdout else None

print("Navigating to first search result...")

# After search, we need to tab to the first result
# Usually takes a few tabs to get to the first result link
time.sleep(2)  # Wait for search results to load

# Tab to navigate to first result (adjust number based on Kinic's interface)
for i in range(3):  # Try 3 tabs to get to first result
    send_keys("{TAB}")
    time.sleep(0.3)

# Select the URL/link text (try different methods)
print("Attempting to select and copy the first result...")

# Method 1: Try to select all on current focused element
send_keys("^a")  # Ctrl+A to select all
time.sleep(0.5)
copy_to_clipboard()  # Ctrl+C to copy
time.sleep(0.5)

# Get the clipboard content
url = get_clipboard()

if url:
    print(f"\n✅ First result URL: {url}")
else:
    print("\n❌ Could not extract URL. The result might not be a direct link.")
    print("You may need to manually check the Kinic interface.")

# Close Kinic
send_keys("{ESC}")
print("\nKinic closed.")