#!/usr/bin/env python3
"""Test ultra-fast triple-click timing"""

import subprocess
import time
import json
import os

def windows_triple_click(x, y, delay_ms=30):
    """Triple-click with configurable delay between clicks"""
    ps_script = f"""
    Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        using System.Threading;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern bool SetCursorPos(int X, int Y);
            
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);
            
            public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
            public const uint MOUSEEVENTF_LEFTUP = 0x0004;
            
            public static void TripleClick(int x, int y, int delayMs) {{
                SetCursorPos(x, y);
                Thread.Sleep(50);
                
                // First click
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                Thread.Sleep(10);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                
                // Delay between clicks
                Thread.Sleep(delayMs);
                
                // Second click
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                Thread.Sleep(10);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                
                // Delay between clicks
                Thread.Sleep(delayMs);
                
                // Third click
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                Thread.Sleep(10);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
            }}
        }}
'@
    [Win32]::TripleClick({x}, {y}, {delay_ms})
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
    return result.stdout.strip() if result.stdout else ""

def clear_clipboard():
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    '''
    subprocess.run(['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-Command', ps_script], capture_output=True)

print("""
╔════════════════════════════════════════════════╗
║     ULTRA-FAST TRIPLE-CLICK TEST              ║
╚════════════════════════════════════════════════╝

Testing different ultra-fast triple-click timings...
Make sure Kinic has an AI response visible!
""")

# Load config
config_file = os.path.expanduser("~/.kinic/config.json")
with open(config_file, 'r') as f:
    config = json.load(f)

ai_x = config['ai_response_x']
ai_y = config['ai_response_y']

print(f"AI Response position: ({ai_x}, {ai_y})")

# Test different timings
timings = [20, 30, 40, 50, 75, 100]
results = []

for timing in timings:
    print(f"\nTesting {timing}ms delay between clicks...")
    clear_clipboard()
    time.sleep(1)
    
    # Triple-click with specified timing
    windows_triple_click(ai_x, ai_y, timing)
    time.sleep(1)
    
    # Copy
    send_keys("^c")
    time.sleep(1)
    
    # Get result
    text = get_clipboard()
    char_count = len(text)
    results.append((timing, char_count, text[:50] if text else ""))
    print(f"  Result: {char_count} characters captured")
    
    # Clear selection for next test
    send_keys("{ESC}")
    time.sleep(1)

print("\n" + "="*60)
print("SUMMARY OF ALL TIMINGS:")
print("="*60)

for timing, chars, preview in results:
    if chars > 0:
        print(f"✅ {timing}ms: {chars} chars - '{preview}...'")
    else:
        print(f"❌ {timing}ms: No text captured")

# Find best result
best = max(results, key=lambda x: x[1])
if best[1] > 0:
    print(f"\n🏆 BEST RESULT: {best[0]}ms with {best[1]} characters")
else:
    print("\n❌ No timing captured any text!")

print("="*60)

# Close Kinic
send_keys("{ESC}")