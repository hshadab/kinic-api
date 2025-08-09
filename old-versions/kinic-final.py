#!/usr/bin/env python3
"""Kinic Desktop v7 - Working Build Version"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
import json
import webbrowser
from datetime import datetime
import time

# Handle imports that might fail in PyInstaller
try:
    import pyautogui
    pyautogui.FAILSAFE = False
except:
    pyautogui = None

try:
    from PIL import Image, ImageDraw, ImageTk
except:
    Image = ImageDraw = ImageTk = None

try:
    import requests
except:
    requests = None

try:
    import pyperclip
except:
    pyperclip = None

COLORS = {
    'primary': '#6366F1',
    'primary_dark': '#4F46E5',
    'background': '#FFFFFF',
    'text_primary': '#0F172A',
    'text_secondary': '#64748B',
    'success': '#10B981',
    'error': '#EF4444',
    'border': '#E2E8F0',
}

class KinicDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kinic Desktop")
        self.root.geometry("1000x800")
        self.root.configure(bg=COLORS['background'])
        
        self.config_file = os.path.expanduser("~/.kinic/config.json")
        self.ensure_config_dir()
        self.load_config()
        
        self.api_running = False
        self.api_port = 5000
        self.api_process = None
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def ensure_config_dir(self):
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
    
    def load_config(self):
        default_config = {'kinic_x': None, 'kinic_y': None}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        # Header - NO subtitle
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Kinic Desktop", 
                font=('Arial', 28, 'bold'),
                bg=COLORS['primary'], fg='white').pack(expand=True)
        
        # Main container
        main = tk.Frame(self.root, bg=COLORS['background'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Setup section
        setup_frame = tk.LabelFrame(main, text="⚙️ Setup", 
                                   font=('Arial', 14, 'bold'),
                                   bg=COLORS['background'], padx=20, pady=15)
        setup_frame.pack(fill=tk.X, pady=(0, 15))
        
        if self.is_configured():
            config_frame = tk.Frame(setup_frame, bg=COLORS['background'])
            config_frame.pack()
            tk.Label(config_frame, text="✓", font=('Arial', 16), 
                    bg=COLORS['background'], fg=COLORS['success']).pack(side=tk.LEFT)
            tk.Label(config_frame, 
                    text=f"Position: ({self.config['kinic_x']}, {self.config['kinic_y']})",
                    font=('Arial', 12), bg=COLORS['background']).pack(side=tk.LEFT, padx=10)
            tk.Button(setup_frame, text="Reconfigure", command=self.setup_position,
                     bg=COLORS['primary'], fg='white', font=('Arial', 11),
                     padx=15, pady=8).pack(pady=10)
        else:
            tk.Label(setup_frame, text="⚠️ Setup required", 
                    font=('Arial', 12), bg=COLORS['background'], 
                    fg=COLORS['error']).pack(pady=5)
            tk.Button(setup_frame, text="Setup Position", command=self.setup_position,
                     bg=COLORS['primary'], fg='white', font=('Arial', 11, 'bold'),
                     padx=20, pady=10).pack(pady=10)
        
        # API Server section
        api_frame = tk.LabelFrame(main, text="🚀 API Server", 
                                 font=('Arial', 14, 'bold'),
                                 bg=COLORS['background'], padx=20, pady=15)
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.api_status_label = tk.Label(api_frame, text="● Server Stopped", 
                                         font=('Arial', 12),
                                         bg=COLORS['background'], 
                                         fg=COLORS['text_secondary'])
        self.api_status_label.pack(pady=5)
        
        self.api_button = tk.Button(api_frame, text="Start API Server", 
                                   command=self.toggle_api,
                                   bg=COLORS['success'], fg='white',
                                   font=('Arial', 11, 'bold'),
                                   padx=20, pady=10)
        self.api_button.pack(pady=10)
        
        # Actions section - NO regular Search
        actions_frame = tk.LabelFrame(main, text="⚡ Actions", 
                                     font=('Arial', 14, 'bold'),
                                     bg=COLORS['background'], padx=20, pady=15)
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Save Page
        save_frame = tk.Frame(actions_frame, bg=COLORS['background'])
        save_frame.pack(fill=tk.X, pady=10)
        tk.Button(save_frame, text="💾 Save Current Page", 
                 command=self.save_page,
                 bg=COLORS['primary'], fg='white',
                 font=('Arial', 12, 'bold'),
                 padx=30, pady=12).pack()
        
        # Search and Retrieve URL (renamed from Get First URL)
        search_frame = tk.Frame(actions_frame, bg=COLORS['background'])
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Search and Retrieve URL:", 
                font=('Arial', 12),
                bg=COLORS['background']).pack(pady=5)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=40)
        self.search_entry.pack(pady=5)
        
        tk.Button(search_frame, text="🔗 Search and Retrieve URL", 
                 command=self.search_retrieve_url,
                 bg=COLORS['primary'], fg='white',
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=10).pack(pady=5)
        
        # Results
        results_frame = tk.LabelFrame(main, text="📊 Results", 
                                     font=('Arial', 14, 'bold'),
                                     bg=COLORS['background'], padx=20, pady=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                      height=10, width=80,
                                                      font=('Consolas', 10),
                                                      bg='#F8F9FA')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.log("Kinic Desktop ready!")
    
    def is_configured(self):
        return self.config.get('kinic_x') is not None
    
    def focus_chrome(self):
        """Focus Chrome window before any action"""
        if not pyautogui:
            return
        try:
            # Click in browser area to ensure focus
            if self.config.get('kinic_x') and self.config.get('kinic_y'):
                pyautogui.click(self.config['kinic_x'] - 200, self.config['kinic_y'])
                time.sleep(0.2)
        except:
            pass
    
    def setup_position(self):
        if not pyautogui:
            messagebox.showerror("Error", "pyautogui module not available!")
            return
            
        messagebox.showinfo("Setup", 
            "1. Open Chrome with Kinic visible\n"
            "2. Click OK\n"
            "3. Hover over Kinic icon within 5 seconds")
        
        self.log("Starting position setup...")
        
        for i in range(5, 0, -1):
            self.log(f"Capturing in {i} seconds...")
            self.root.update()
            time.sleep(1)
        
        x, y = pyautogui.position()
        self.config['kinic_x'] = x
        self.config['kinic_y'] = y
        self.save_config()
        
        self.log(f"✓ Position saved: ({x}, {y})")
        messagebox.showinfo("Success", f"Position saved: ({x}, {y})")
        
        # Refresh UI
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def toggle_api(self):
        if self.api_running:
            self.stop_api()
        else:
            self.start_api()
    
    def start_api(self):
        if not self.is_configured():
            messagebox.showerror("Error", "Please setup position first!")
            return
        
        self.log("Starting API server...")
        
        # Create API server code
        api_code = f"""
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import time
import pyperclip

app = Flask(__name__)
CORS(app)

KINIC_X = {self.config.get('kinic_x', 0)}
KINIC_Y = {self.config.get('kinic_y', 0)}

pyautogui.FAILSAFE = False

def focus_chrome_and_prepare():
    # Focus Chrome and press ESC
    pyautogui.press('escape')
    time.sleep(1)  # 1 second delay after ESC

@app.route('/health')
def health():
    return jsonify({{'status': 'ok'}})

@app.route('/api/save', methods=['POST'])
def save():
    focus_chrome_and_prepare()
    pyautogui.click(KINIC_X, KINIC_Y)
    time.sleep(0.8)
    pyautogui.hotkey('shift', 'tab')
    time.sleep(0.3)
    pyautogui.press('enter')
    return jsonify({{'success': True, 'message': 'Page saved'}})

@app.route('/api/search-retrieve-url', methods=['POST'])
def search_retrieve_url():
    data = request.json or {{}}
    query = data.get('query', '')
    
    focus_chrome_and_prepare()
    pyautogui.click(KINIC_X, KINIC_Y)
    time.sleep(0.8)
    
    # Tab 4 times
    for _ in range(4):
        pyautogui.press('tab')
        time.sleep(0.2)
    
    pyautogui.typewrite(query)
    pyautogui.press('enter')
    time.sleep(3)  # Wait 3 seconds
    
    # Tab 2 times
    pyautogui.press('tab')
    time.sleep(0.2)
    pyautogui.press('tab')
    time.sleep(0.3)
    
    # Shift+Fn+F10
    pyautogui.hotkey('shift', 'fn', 'f10')
    time.sleep(2)  # Wait 2 seconds
    
    # Down 5 times
    for _ in range(5):
        pyautogui.press('down')
        time.sleep(0.2)
    
    pyautogui.press('enter')
    time.sleep(0.5)
    
    url = pyperclip.paste()
    return jsonify({{'success': True, 'url': url}})

if __name__ == '__main__':
    app.run(port=5000, debug=False)
"""
        
        # Save and run
        api_file = os.path.join(os.path.dirname(self.config_file), "api_server.py")
        with open(api_file, 'w') as f:
            f.write(api_code)
        
        self.api_process = subprocess.Popen([sys.executable, api_file],
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
        
        time.sleep(2)
        self.api_running = True
        self.api_status_label.config(text="● Server Running", fg=COLORS['success'])
        self.api_button.config(text="Stop API Server", bg=COLORS['error'])
        self.log("✓ API server started on port 5000")
    
    def stop_api(self):
        if self.api_process:
            self.api_process.terminate()
            self.api_process = None
        
        self.api_running = False
        self.api_status_label.config(text="● Server Stopped", fg=COLORS['text_secondary'])
        self.api_button.config(text="Start API Server", bg=COLORS['success'])
        self.log("API server stopped")
    
    def save_page(self):
        if not self.is_configured():
            messagebox.showerror("Error", "Please setup position first!")
            return
        
        if not pyautogui:
            messagebox.showerror("Error", "pyautogui not available!")
            return
        
        def do_save():
            self.log("Saving page...")
            
            # Focus Chrome and ESC with 1 second delay
            self.focus_chrome()
            pyautogui.press('escape')
            time.sleep(1)
            
            # Click Kinic
            pyautogui.click(self.config['kinic_x'], self.config['kinic_y'])
            time.sleep(0.8)
            
            # Shift+Tab, Enter
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.3)
            pyautogui.press('enter')
            
            self.log("✓ Page saved!")
        
        thread = threading.Thread(target=do_save)
        thread.daemon = True
        thread.start()
    
    def search_retrieve_url(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        if not self.is_configured():
            messagebox.showerror("Error", "Please setup position first!")
            return
        
        if not pyautogui:
            messagebox.showerror("Error", "pyautogui not available!")
            return
        
        def do_search():
            self.log(f"Searching and retrieving URL for: {query}")
            
            # Focus Chrome and ESC with 1 second delay
            self.focus_chrome()
            pyautogui.press('escape')
            time.sleep(1)
            
            # Click Kinic
            pyautogui.click(self.config['kinic_x'], self.config['kinic_y'])
            time.sleep(0.8)
            
            # Tab 4 times
            for _ in range(4):
                pyautogui.press('tab')
                time.sleep(0.2)
            
            # Type and search
            pyautogui.typewrite(query)
            pyautogui.press('enter')
            
            # Wait 3 seconds
            time.sleep(3)
            
            # Tab 2 times
            pyautogui.press('tab')
            time.sleep(0.2)
            pyautogui.press('tab')
            time.sleep(0.3)
            
            # Shift+Fn+F10
            pyautogui.hotkey('shift', 'fn', 'f10')
            time.sleep(2)
            
            # Down 5 times
            for _ in range(5):
                pyautogui.press('down')
                time.sleep(0.2)
            
            # Enter
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Get URL
            if pyperclip:
                url = pyperclip.paste()
                self.log(f"✓ URL retrieved: {url}")
            else:
                self.log("✓ URL copied to clipboard")
        
        thread = threading.Thread(target=do_search)
        thread.daemon = True
        thread.start()
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def on_closing(self):
        if self.api_running:
            self.stop_api()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KinicDesktop()
    app.run()