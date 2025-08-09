#!/usr/bin/env python3
"""Open a URL in Chrome and save it to Kinic"""

import subprocess
import time
import sys

def open_url_in_chrome(url):
    """Open URL in Chrome using Windows"""
    ps_script = f"""
    Start-Process "chrome.exe" -ArgumentList "{url}"
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def focus_chrome():
    """Focus Chrome window"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            
            [DllImport("user32.dll")]
            public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        }
'@
    Start-Sleep -Milliseconds 500
    $chrome = [Win32]::FindWindow("Chrome_WidgetWin_1", $null)
    if ($chrome -ne [IntPtr]::Zero) {
        [Win32]::SetForegroundWindow($chrome)
    }
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

# Open the URL
url = "https://github.com/hshadab/verifiable-agentkit"
print(f"Opening {url} in Chrome...")
open_url_in_chrome(url)

# Wait for page to load
print("Waiting for page to load...")
time.sleep(4)

# Focus Chrome
print("Focusing Chrome...")
focus_chrome()
time.sleep(1)

print("Done! Page should be open in Chrome.")
print("\nNow saving to Kinic...")