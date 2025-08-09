#!/usr/bin/env python3
"""Search and retrieve URL from Kinic using the correct sequence"""

import subprocess
import time
import sys
import json

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

def click_kinic():
    """Click Kinic button"""
    ps_script = f"""
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern bool SetCursorPos(int X, int Y);
            
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);
            
            public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
            public const uint MOUSEEVENTF_LEFTUP = 0x0004;
        }}
'@
    [Win32]::SetCursorPos(959, 98)
    Start-Sleep -Milliseconds 100
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 50
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def send_shift_fn_f10():
    """Send Shift+Fn+F10 for context menu"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("+{F10}")
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

def search_and_retrieve(search_term):
    """Execute the full search and retrieve sequence"""
    print(f"Searching for '{search_term}' and retrieving first URL...")
    
    # Step 1: Open Kinic
    print("1. Opening Kinic...")
    click_kinic()
    time.sleep(2)
    
    # Step 2: Tab 4 times to search field
    print("2. Navigating to search field (Tab x4)...")
    for i in range(4):
        send_keys("{TAB}")
        time.sleep(0.2)
    
    # Step 3: Enter search term
    print(f"3. Entering search term: {search_term}")
    send_keys(search_term)
    time.sleep(0.5)
    
    # Step 4: Press Enter
    print("4. Pressing Enter to search...")
    send_keys("{ENTER}")
    
    # Step 5: Wait 3 seconds for results
    print("5. Waiting 3 seconds for results to load...")
    time.sleep(3)
    
    # Step 6: Tab 2 times to first result
    print("6. Navigating to first result (Tab x2)...")
    for i in range(2):
        send_keys("{TAB}")
        time.sleep(0.3)
    
    # Step 7: Shift+Fn+F10 for context menu
    print("7. Opening context menu (Shift+Fn+F10)...")
    send_shift_fn_f10()
    
    # Step 8: Wait 2 seconds
    print("8. Waiting 2 seconds for context menu...")
    time.sleep(2)
    
    # Step 9: Down arrow 5 times
    print("9. Navigating context menu (Down x5)...")
    for i in range(5):
        send_keys("{DOWN}")
        time.sleep(0.2)
    
    # Step 10: Enter to copy URL
    print("10. Pressing Enter to copy URL...")
    send_keys("{ENTER}")
    time.sleep(1)
    
    # Step 11: Extract copied URL
    print("11. Extracting URL from clipboard...")
    url = get_clipboard()
    
    # Close Kinic
    send_keys("{ESC}")
    
    return url

if __name__ == "__main__":
    # Get search term from command line or use default
    search_term = sys.argv[1] if len(sys.argv) > 1 else "code"
    
    url = search_and_retrieve(search_term)
    
    # Output as JSON
    result = {
        "search_term": search_term,
        "url": url,
        "success": bool(url)
    }
    
    print("\n" + "=" * 60)
    print("RESULT:")
    print(json.dumps(result, indent=2))
    
    if url:
        print(f"\n✅ First URL for '{search_term}': {url}")
    else:
        print(f"\n❌ Could not retrieve URL for '{search_term}'")