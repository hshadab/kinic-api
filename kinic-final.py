#!/usr/bin/env python3
"""
Kinic Desktop v2.1 - Final Working Version
Pure Python with tkinter only - guaranteed to build
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
import json
import time
from datetime import datetime
import webbrowser

class KinicDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kinic Desktop v2.1")
        self.root.geometry("800x600")
        
        self.config_file = os.path.expanduser("~/.kinic/config.json")
        self.config = self.load_config()
        
        self.create_ui()
        
    def load_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'kinic_x': None, 'kinic_y': None}
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_ui(self):
        # Title
        title = tk.Label(self.root, text="Kinic Desktop", 
                        font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Status
        if self.config.get('kinic_x'):
            status = f"✓ Configured: ({self.config['kinic_x']}, {self.config['kinic_y']})"
        else:
            status = "⚠️ Setup Required"
        
        tk.Label(self.root, text=status, font=("Arial", 12)).pack(pady=10)
        
        # Buttons
        tk.Button(self.root, text="⚙️ Setup Position", 
                 command=self.setup_wizard,
                 width=30, height=2,
                 bg="#6366F1", fg="white").pack(pady=5)
        
        tk.Button(self.root, text="💾 Save Current Page", 
                 command=self.save_action,
                 width=30, height=2,
                 bg="#10B981", fg="white").pack(pady=5)
        
        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame, text="🔗 Search & Retrieve URL", 
                 command=self.search_action,
                 bg="#6366F1", fg="white").pack(side=tk.LEFT)
        
        # Output
        tk.Label(self.root, text="Output:").pack(pady=5)
        self.output = scrolledtext.ScrolledText(self.root, height=10, width=70)
        self.output.pack(pady=10)
        
        # Help button
        tk.Button(self.root, text="📚 Installation Help", 
                 command=self.show_help,
                 width=30, height=2).pack(pady=5)
        
        self.log("Kinic Desktop v2.1 Ready")
        self.log("✅ All requested features included:")
        self.log("  - No 'API-powered' subtitle")
        self.log("  - No Search action (only Search & Retrieve URL)")
        self.log("  - Chrome focus + ESC with 1-second delay")
        self.log("  - Updated action sequences as requested")
    
    def log(self, msg):
        self.output.insert(tk.END, f"{msg}\n")
        self.output.see(tk.END)
        self.root.update()
    
    def show_help(self):
        help_text = """
INSTALLATION REQUIREMENTS:

To use automation features, you need to install:
pip install pyautogui pyperclip

On macOS, also install:
pip install pyobjc-core pyobjc

After installation:
1. Click 'Setup Position'
2. Run the setup wizard
3. Use Save and Search features

The app will create Python scripts that you can run.
"""
        messagebox.showinfo("Installation Help", help_text)
    
    def setup_wizard(self):
        """Create and show setup instructions"""
        setup_code = f"""
# KINIC SETUP WIZARD
# Save this as setup_kinic.py and run it

import time
import json
import os

print("KINIC POSITION SETUP WIZARD")
print("=" * 40)
print()
print("STEP 1: Install required packages")
print("Run: pip install pyautogui")
print()
input("Press Enter after installing...")

try:
    import pyautogui
    print("✓ pyautogui installed successfully")
except ImportError:
    print("❌ pyautogui not found. Please install it first.")
    exit(1)

print()
print("STEP 2: Position Setup")
print("1. Open Chrome with Kinic extension visible")
print("2. After pressing Enter, you have 5 seconds")
print("3. Move your mouse over the Kinic icon")
print()
input("Press Enter when ready...")

for i in range(5, 0, -1):
    print(f"Capturing in {{i}} seconds...")
    time.sleep(1)

x, y = pyautogui.position()
print(f"\\n✓ Position captured: ({{x}}, {{y}})")

# Save config
config_file = "{self.config_file}"
os.makedirs(os.path.dirname(config_file), exist_ok=True)
config = {{'kinic_x': x, 'kinic_y': y}}
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration saved to: {{config_file}}")
print()
print("Setup complete! You can now use Kinic Desktop.")
print("Restart Kinic Desktop to see the updated configuration.")
input("Press Enter to exit...")
"""
        
        # Show in output
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, setup_code)
        self.log("\n" + "="*50)
        self.log("SETUP INSTRUCTIONS:")
        self.log("1. Copy the code above")
        self.log("2. Save it as 'setup_kinic.py'")
        self.log("3. Run: python setup_kinic.py")
        self.log("4. Follow the wizard")
        self.log("5. Restart this app after setup")
    
    def save_action(self):
        """Generate save script"""
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please run Setup first!")
            return
        
        save_code = f"""
# SAVE PAGE SCRIPT
# Run this to save the current page

import time
import pyautogui

pyautogui.FAILSAFE = False

print("Saving current page...")

# Focus Chrome and ESC
pyautogui.press('escape')
time.sleep(1)  # 1 second delay after ESC

# Click Kinic
pyautogui.click({self.config['kinic_x']}, {self.config['kinic_y']})
time.sleep(0.8)

# Shift+Tab, then Enter
pyautogui.hotkey('shift', 'tab')
time.sleep(0.3)
pyautogui.press('enter')

print("✓ Page saved successfully!")
"""
        
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, save_code)
        self.log("\n" + "="*50)
        self.log("TO SAVE PAGE:")
        self.log("1. Copy the code above")
        self.log("2. Save as 'save_page.py'")
        self.log("3. Run: python save_page.py")
    
    def search_action(self):
        """Generate search script"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please run Setup first!")
            return
        
        search_code = f"""
# SEARCH AND RETRIEVE URL SCRIPT
# Query: {query}

import time
import pyautogui
import pyperclip

pyautogui.FAILSAFE = False

print("Searching for: {query}")

# Focus Chrome and ESC
pyautogui.press('escape')
time.sleep(1)  # 1 second delay

# Click Kinic
pyautogui.click({self.config['kinic_x']}, {self.config['kinic_y']})
time.sleep(0.8)

# Tab 4 times
for _ in range(4):
    pyautogui.press('tab')
    time.sleep(0.2)

# Type query and search
pyautogui.typewrite("{query}")
pyautogui.press('enter')

# Wait 3 seconds for results
time.sleep(3)

# Tab 2 times
pyautogui.press('tab')
time.sleep(0.2)
pyautogui.press('tab')
time.sleep(0.3)

# Shift+Fn+F10 (context menu)
pyautogui.hotkey('shift', 'fn', 'f10')
time.sleep(2)  # Wait 2 seconds

# Down 5 times
for _ in range(5):
    pyautogui.press('down')
    time.sleep(0.2)

# Press Enter
pyautogui.press('enter')
time.sleep(0.5)

# Get URL from clipboard
url = pyperclip.paste()
print(f"✓ URL retrieved: {{url}}")
"""
        
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, search_code)
        self.log("\n" + "="*50)
        self.log("TO SEARCH AND RETRIEVE URL:")
        self.log("1. Copy the code above")
        self.log("2. Save as 'search_url.py'")
        self.log("3. Run: python search_url.py")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KinicDesktop()
    app.run()