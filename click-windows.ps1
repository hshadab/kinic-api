# PowerShell script to click in Windows
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;

    public class MouseOperations
    {
        [DllImport("user32.dll", SetLastError = true)]
        static extern uint SendInput(uint nInputs, ref INPUT pInputs, int cbSize);

        [DllImport("user32.dll")]
        static extern bool SetCursorPos(int X, int Y);

        [DllImport("user32.dll")]
        static extern bool SetForegroundWindow(IntPtr hWnd);

        [DllImport("user32.dll")]
        static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

        struct INPUT
        {
            public int type;
            public MOUSEINPUT mi;
        }

        struct MOUSEINPUT
        {
            public int dx;
            public int dy;
            public uint mouseData;
            public uint dwFlags;
            public uint time;
            public IntPtr dwExtraInfo;
        }

        const int INPUT_MOUSE = 0;
        const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
        const uint MOUSEEVENTF_LEFTUP = 0x0004;
        const uint MOUSEEVENTF_ABSOLUTE = 0x8000;

        public static void Click(int x, int y)
        {
            SetCursorPos(x, y);
            
            INPUT input = new INPUT();
            input.type = INPUT_MOUSE;
            input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
            SendInput(1, ref input, Marshal.SizeOf(input));
            
            input.mi.dwFlags = MOUSEEVENTF_LEFTUP;
            SendInput(1, ref input, Marshal.SizeOf(input));
        }

        public static void FocusChrome()
        {
            // Try to find Chrome window
            IntPtr chromeHandle = FindWindow("Chrome_WidgetWin_1", null);
            if (chromeHandle != IntPtr.Zero)
            {
                SetForegroundWindow(chromeHandle);
            }
        }
    }
"@ -ReferencedAssemblies System.Windows.Forms

# Focus Chrome
Write-Host "Focusing Chrome..."
[MouseOperations]::FocusChrome()
Start-Sleep -Milliseconds 500

# Click at Kinic position
Write-Host "Clicking at (904, 96)..."
[MouseOperations]::Click(904, 96)

Write-Host "Done!"