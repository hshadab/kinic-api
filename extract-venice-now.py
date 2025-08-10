#!/usr/bin/env python3
"""Extract the Venice AI response that's currently visible"""

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

def get_clipboard():
    """Get clipboard with proper encoding handling"""
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    $text = [System.Windows.Forms.Clipboard]::GetText()
    [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($text))
    '''
    result = subprocess.run(
        ['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], 
        capture_output=True, 
        text=True,
        errors='replace'  # Handle encoding errors
    )
    
    if result.stdout:
        try:
            import base64
            encoded = result.stdout.strip()
            decoded_bytes = base64.b64decode(encoded)
            return decoded_bytes.decode('utf-8', errors='replace')
        except:
            return result.stdout.strip()
    return "[empty]"

def clear_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

print("""
╔════════════════════════════════════════════════╗
║     EXTRACT VENICE AI RESPONSE                ║
╚════════════════════════════════════════════════╝

Assuming Kinic has Venice AI response visible...
""")

ai_x = config['ai_response_x']
ai_y = config['ai_response_y']

print(f"AI response coordinates: ({ai_x}, {ai_y})")

# Clear clipboard first
print("\nClearing clipboard...")
clear_clipboard()

# Triple-click method
print(f"\nTriple-clicking at ({ai_x}, {ai_y})...")
windows_click(ai_x, ai_y)
time.sleep(0.02)  # 20ms
windows_click(ai_x, ai_y)
time.sleep(0.02)  # 20ms
windows_click(ai_x, ai_y)

print("Waiting 2 seconds for selection...")
time.sleep(2)

print("Copying with Ctrl+C...")
send_keys("^c")

print("Waiting 2 seconds for copy...")
time.sleep(2)

print("Getting clipboard content...")
text = get_clipboard()

print("\n" + "="*60)
print("RESULT:")
print("="*60)

if text and text != "[empty]" and len(text) > 10:
    print(f"✅ Successfully captured {len(text)} characters!")
    print("\nVenice AI Response:")
    print("-"*40)
    print(text)
    print("-"*40)
    
    # Save to file
    with open("venice-response.txt", "w", encoding='utf-8') as f:
        f.write(text)
    print("\n📄 Saved to venice-response.txt")
else:
    print(f"❌ Failed to capture AI text")
    print(f"   Clipboard contains: '{text}'")