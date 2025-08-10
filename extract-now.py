#!/usr/bin/env python3
"""Extract AI text right now with mouse at current position"""

import subprocess
import time

def triple_click():
    """Triple-click at current mouse position"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        using System.Threading;
        
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);
            
            public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
            public const uint MOUSEEVENTF_LEFTUP = 0x0004;
        }
'@
    # First click
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 10
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    # 20ms delay
    Start-Sleep -Milliseconds 20
    
    # Second click
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 10
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    # 20ms delay
    Start-Sleep -Milliseconds 20
    
    # Third click
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 10
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

print("Extracting AI text NOW!")
print("Keep your mouse on the AI response!")

# Clear clipboard first
clear_clipboard()

# Triple-click
print("\nTriple-clicking...")
triple_click()

# Wait for selection
time.sleep(2)

# Copy
print("Copying...")
send_keys("^c")

# Wait for copy
time.sleep(2)

# Get result
print("Getting clipboard...")
result = get_clipboard()

print("\n" + "="*60)
print("EXTRACTED TEXT:")
print("="*60)

if result and result != "[empty]":
    print(f"✅ Captured {len(result)} characters:\n")
    print(result[:500])
    if len(result) > 500:
        print("\n... (truncated)")
else:
    print("❌ No text captured")

print("="*60)