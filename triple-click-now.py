#!/usr/bin/env python3
"""Triple-click at current mouse position"""

import subprocess
import time

def triple_click():
    """Triple-click at current mouse position with ultra-fast timing"""
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

print("Triple-clicking in 2 seconds...")
print("Keep your mouse on the AI response!")
time.sleep(2)

triple_click()
print("✅ Triple-click done!")