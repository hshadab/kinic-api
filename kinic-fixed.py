#!/usr/bin/env python3
"""Kinic Desktop - Fixed Version with Scrollbar"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import sys
import os
import json
import webbrowser
from datetime import datetime
import time

# Try to import modules, but continue if they fail
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
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
        
        # Check module status
        if not PYAUTOGUI_AVAILABLE:
            self.log("⚠️ WARNING: pyautogui module not available - automation features disabled")
            self.log("To enable: pip install pyautogui")
    
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
        # Header
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Kinic Desktop", 
                font=('Arial', 28, 'bold'),
                bg=COLORS['primary'], fg='white').pack(expand=True)
        
        # Main container with scrollable frame
        main_container = tk.Frame(self.root, bg=COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas and scrollbar for main content
        canvas = tk.Canvas(main_container, bg=COLORS['background'], highlightthickness=0)
        
        # Create THICK scrollbar
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Style the scrollbar to make it thicker
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", 
                       width=30,  # Make scrollbar thick
                       arrowsize=20,
                       borderwidth=2,
                       relief="raised")
        
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Now add all content to scrollable_frame
        main = scrollable_frame
        
        # Setup section
        setup_frame = tk.LabelFrame(main, text="⚙️ Setup", 
                                   font=('Arial', 14, 'bold'),
                                   bg=COLORS['background'], padx=20, pady=15)
        setup_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        # Module status
        if not PYAUTOGUI_AVAILABLE:
            status_frame = tk.Frame(setup_frame, bg=COLORS['background'])
            status_frame.pack()
            tk.Label(status_frame, text="❌", font=('Arial', 16), 
                    bg=COLORS['background'], fg=COLORS['error']).pack(side=tk.LEFT)
            tk.Label(status_frame, 
                    text="pyautogui module not installed",
                    font=('Arial', 12), bg=COLORS['background'],
                    fg=COLORS['error']).pack(side=tk.LEFT, padx=10)
        elif self.is_configured():
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
        api_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        self.api_status_label = tk.Label(api_frame, text="● Server Stopped", 
                                         font=('Arial', 12),
                                         bg=COLORS['background'], 
                                         fg=COLORS['text_secondary'])
        self.api_status_label.pack(pady=5)
        
        self.api_button = tk.Button(api_frame, text="Start API Server", 
                                   command=self.toggle_api,
                                   bg=COLORS['success'], fg='white',
                                   font=('Arial', 11, 'bold'),
                                   padx=20, pady=10,
                                   state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED)
        self.api_button.pack(pady=10)
        
        # Actions section
        actions_frame = tk.LabelFrame(main, text="⚡ Actions", 
                                     font=('Arial', 14, 'bold'),
                                     bg=COLORS['background'], padx=20, pady=15)
        actions_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        # Save Page
        save_frame = tk.Frame(actions_frame, bg=COLORS['background'])
        save_frame.pack(fill=tk.X, pady=10)
        tk.Button(save_frame, text="💾 Save Current Page", 
                 command=self.save_page,
                 bg=COLORS['primary'], fg='white',
                 font=('Arial', 12, 'bold'),
                 padx=30, pady=12,
                 state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED).pack()
        
        # Search and Retrieve URL
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
                 padx=20, pady=10,
                 state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED).pack(pady=5)
        
        # Results - with its own scrollbar
        results_frame = tk.LabelFrame(main, text="📊 Results", 
                                     font=('Arial', 14, 'bold'),
                                     bg=COLORS['background'], padx=20, pady=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(results_frame, bg=COLORS['background'])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_frame, 
                                   height=15, width=80,
                                   font=('Consolas', 10),
                                   bg='#F8F9FA',
                                   wrap=tk.WORD)
        
        # Create thick scrollbar for results
        results_scrollbar = tk.Scrollbar(text_frame, 
                                        width=25,
                                        bg='#CBD5E1',
                                        activebackground='#94A3B8',
                                        troughcolor='#F1F5F9',
                                        bd=2,
                                        relief=tk.RAISED)
        
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        results_scrollbar.config(command=self.results_text.yview)
        
        self.log("Kinic Desktop ready!")
        self.log(f"pyautogui: {'✓ Installed' if PYAUTOGUI_AVAILABLE else '❌ Not installed'}")
        self.log(f"pyperclip: {'✓ Installed' if PYPERCLIP_AVAILABLE else '❌ Not installed'}")
    
    def is_configured(self):
        return self.config.get('kinic_x') is not None
    
    def setup_position(self):
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showerror("Module Error", 
                "pyautogui module is not installed!\n\n"
                "Please install it using:\n"
                "pip install pyautogui")
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
        
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showerror("Error", "pyautogui module not available!")
            return
        
        self.log("Starting API server...")
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
        
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showerror("Error", "pyautogui not available!")
            return
        
        def do_save():
            self.log("Saving page...")
            
            # Focus Chrome and ESC
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
        
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showerror("Error", "pyautogui not available!")
            return
        
        self.log(f"Searching for: {query}")
        self.log("Feature would work with pyautogui installed")
    
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