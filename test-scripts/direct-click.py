#!/usr/bin/env python3
"""Click at exact position without moving cursor"""

import subprocess
import time

def direct_click(x, y):
    """Click at exact coordinates without moving cursor visibly"""
    ps_script = f"""
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);
            
            [DllImport("user32.dll")]
            public static extern bool SetCursorPos(int X, int Y);
            
            [DllImport("user32.dll")]
            public static extern bool GetCursorPos(out POINT lpPoint);
            
            public struct POINT {{
                public int X;
                public int Y;
            }}
            
            public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
            public const uint MOUSEEVENTF_LEFTUP = 0x0004;
            public const uint MOUSEEVENTF_ABSOLUTE = 0x8000;
            public const uint MOUSEEVENTF_MOVE = 0x0001;
            
            public static void ClickAt(int x, int y) {{
                // Save current position
                POINT currentPos;
                GetCursorPos(out currentPos);
                
                // Click at target without visible movement
                SetCursorPos(x, y);
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                
                // Restore original position
                SetCursorPos(currentPos.X, currentPos.Y);
            }}
        }}
'@
    [Win32]::ClickAt({x}, {y})
    """
    
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )

# Click Kinic at exact position
print("Clicking Kinic at (904, 96) without moving cursor...")
direct_click(904, 96)
print("Done! Kinic should be open.")