#!/usr/bin/env python3
"""Debug script for AI extraction workflow - shows each step clearly"""

import subprocess
import time
import json
import os

def windows_click(x, y):
    """Click at exact position"""
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
    [Win32]::SetCursorPos({x}, {y})
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

def send_keys(keys):
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{keys}")
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

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
    $chrome = Get-Process chrome | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object -First 1
    if ($chrome) {
        [Win32]::SetForegroundWindow($chrome.MainWindowHandle)
    }
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

def get_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    '''
    result = subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "[empty]"

def clear_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

def wait_with_countdown(seconds, message):
    """Show countdown while waiting"""
    print(f"{message} ({seconds}s)")
    for i in range(seconds, 0, -1):
        print(f"  {i}...", end='\r')
        time.sleep(1)
    print("  Done!    ")

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════════════════╗
║     DEBUG: AI EXTRACTION WORKFLOW                         ║
╠════════════════════════════════════════════════════════════╣
║  This will show exactly what happens at each step         ║
║  Watch carefully to see where things might be going wrong ║
╚════════════════════════════════════════════════════════════╝

Current Configuration:
""")
print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
print(f"  AI response:  ({config['ai_response_x']}, {config['ai_response_y']})")
print("\n" + "="*60)

# Step 1: Focus Chrome
print("\n📍 STEP 1: Focus Chrome window")
focus_chrome()
wait_with_countdown(2, "  Waiting for Chrome to focus")

# Step 2: Close any existing popup
print("\n📍 STEP 2: Press ESC to close any existing Kinic popup")
send_keys("{ESC}")
wait_with_countdown(2, "  Waiting after ESC")

# Step 3: Open Kinic
print(f"\n📍 STEP 3: Click Kinic button at ({config['kinic_x']}, {config['kinic_y']})")
windows_click(config['kinic_x'], config['kinic_y'])
wait_with_countdown(3, "  Waiting for Kinic to fully load")

# Step 4: Navigate to search
print("\n📍 STEP 4: Navigate to search field (TAB 4 times)")
for i in range(4):
    print(f"  TAB {i+1}/4")
    send_keys("{TAB}")
    time.sleep(0.5)
wait_with_countdown(2, "  Waiting after navigation")

# Step 5: Type search query
query = "quantum computing"
print(f"\n📍 STEP 5: Type search query: '{query}'")
send_keys(query)
wait_with_countdown(2, "  Waiting after typing")
print("  Pressing ENTER to search")
send_keys("{ENTER}")

# Step 6: Wait for results
print("\n📍 STEP 6: Wait for search results")
wait_with_countdown(4, "  Loading search results")

# Step 7: Navigate to AI button
print("\n📍 STEP 7: Navigate to AI button (TAB 5 times)")
for i in range(5):
    print(f"  TAB {i+1}/5")
    send_keys("{TAB}")
    time.sleep(0.5)
wait_with_countdown(2, "  Waiting after navigation")

# Step 8: Click AI button
print("\n📍 STEP 8: Press ENTER to activate AI")
send_keys("{ENTER}")

# Step 9: Wait for AI response
print("\n📍 STEP 9: Wait for AI to generate response")
print("  ⚠️  WATCH: Is the AI response appearing?")
print("  ⚠️  WATCH: Where does it appear on screen?")
wait_with_countdown(10, "  Generating AI response")

# Step 10: Triple-click to select
print(f"\n📍 STEP 10: Triple-click at ({config['ai_response_x']}, {config['ai_response_y']})")
print("  ⚠️  WATCH: Is the mouse clicking in the right place?")
print("  First click...")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.02)  # 20ms
print("  Second click...")
windows_click(config['ai_response_x'], config['ai_response_y'])
time.sleep(0.02)  # 20ms
print("  Third click...")
windows_click(config['ai_response_x'], config['ai_response_y'])
wait_with_countdown(2, "  Waiting after selection")

# Step 11: Copy to clipboard
print("\n📍 STEP 11: Copy selected text (Ctrl+C)")
clear_clipboard()  # Clear first to ensure we get new content
send_keys("^c")
wait_with_countdown(2, "  Waiting for copy")

# Step 12: Check what was copied
print("\n📍 STEP 12: Check clipboard contents")
captured_text = get_clipboard()

print("\n" + "="*60)
print("RESULTS:")
print("="*60)

if captured_text and captured_text != "[empty]":
    print(f"✅ Captured {len(captured_text)} characters")
    print(f"\nFirst 200 characters:")
    print("-" * 40)
    print(captured_text[:200])
    if len(captured_text) > 200:
        print("...")
    print("-" * 40)
    
    # Check if it's a URL
    if captured_text.startswith("http"):
        print("\n⚠️  WARNING: Captured text appears to be a URL!")
        print("   The mouse might be clicking on a search result instead of AI response")
else:
    print("❌ No text was captured!")
    print("\nPossible issues:")
    print("  1. AI response coordinates are wrong")
    print("  2. AI didn't generate a response")
    print("  3. Triple-click didn't select the text")
    print("  4. The AI response area requires different selection method")

print("\n" + "="*60)
print("TROUBLESHOOTING TIPS:")
print("="*60)
print("""
If the AI text wasn't captured correctly:

1. Check if the AI response actually appeared
   - Did you see text generated after Step 9?
   
2. Check if the mouse clicked in the right place
   - Was the cursor in the AI response area at Step 10?
   
3. Try manual positioning:
   - Put your mouse on the AI response text
   - Run: python capture-now.py
   - Then run: python setup-ai-position.py
   
4. Check if more wait time is needed:
   - AI might need more than 10 seconds
   - Try increasing the wait in Step 9
""")

# Step 13: Close Kinic
print("\n📍 STEP 13: Close Kinic")
send_keys("{ESC}")

print("\n✅ Debug session complete!")
print("\nNext steps:")
print("1. Review what happened at each step")
print("2. Note where things went wrong")
print("3. Adjust coordinates or timing as needed")