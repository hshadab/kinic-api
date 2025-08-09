#!/usr/bin/env python3
"""Windows clicker using PowerShell for actual Windows interaction"""

import subprocess
import json
import time
import os

def powershell_click(x, y):
    """Click using Windows PowerShell"""
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
    [Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    Write-Host "Clicked at ({x}, {y})"
    """
    
    try:
        result = subprocess.run(
            ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", 
             "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True, text=True, timeout=5
        )
        print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return True
    except Exception as e:
        print(f"Failed to click: {e}")
        return False

def focus_chrome():
    """Focus Chrome window"""
    ps_script = """
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            
            [DllImport("user32.dll")]
            public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        }}
'@
    $chrome = [Win32]::FindWindow("Chrome_WidgetWin_1", $null)
    if ($chrome -ne [IntPtr]::Zero) {{
        [Win32]::SetForegroundWindow($chrome)
        Write-Host "Chrome focused"
    }} else {{
        Write-Host "Chrome window not found"
    }}
    """
    
    try:
        subprocess.run(
            ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
             "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True, text=True, timeout=5
        )
        return True
    except:
        return False

def click_kinic():
    """Click the Kinic extension button"""
    print("Focusing Chrome window...")
    focus_chrome()
    time.sleep(0.5)
    
    print("Clicking Kinic button at (904, 96)...")
    powershell_click(904, 96)
    
    print("Done!")

if __name__ == "__main__":
    click_kinic()