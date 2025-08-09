#!/usr/bin/env python3
"""Kinic Desktop - Fully Working Version"""

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

# Try to import modules
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None
    print(f"pyautogui not available: {e}")

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except:
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
        self.root.geometry("1000x900")
        self.root.configure(bg=COLORS['background'])
        
        self.config_file = os.path.expanduser("~/.kinic/config.json")
        self.ensure_config_dir()
        self.load_config()
        
        self.api_running = False
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        if PYAUTOGUI_AVAILABLE:
            self.log("✅ pyautogui module loaded successfully")
            self.test_mouse_movement()
        else:
            self.log("❌ pyautogui module not available")
    
    def test_mouse_movement(self):
        """Test if mouse movement works"""
        try:
            current_pos = pyautogui.position()
            self.log(f"Current mouse position: {current_pos}")
            # Small test movement
            pyautogui.moveRel(1, 1, duration=0.1)
            pyautogui.moveRel(-1, -1, duration=0.1)
            self.log("✅ Mouse movement test successful")
        except Exception as e:
            self.log(f"⚠️ Mouse movement error: {e}")
    
    def test_mouse_action(self):
        """Test mouse movement from button click"""
        try:
            self.log("Testing mouse movement...")
            
            # Get current position
            start_pos = pyautogui.position()
            self.log(f"Starting position: {start_pos}")
            
            # Move in a square pattern
            self.log("Moving right 200px...")
            pyautogui.moveTo(start_pos.x + 200, start_pos.y, duration=0.5)
            self.root.update()
            
            self.log("Moving down 200px...")
            pyautogui.moveTo(start_pos.x + 200, start_pos.y + 200, duration=0.5)
            self.root.update()
            
            self.log("Moving left 200px...")
            pyautogui.moveTo(start_pos.x, start_pos.y + 200, duration=0.5)
            self.root.update()
            
            self.log("Moving back to start...")
            pyautogui.moveTo(start_pos.x, start_pos.y, duration=0.5)
            self.root.update()
            
            self.log("✅ Mouse movement test complete!")
            
        except Exception as e:
            self.log(f"❌ Mouse test error: {e}")
            import traceback
            self.log(traceback.format_exc())
            
    def ensure_config_dir(self):
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
    
    def load_config(self):
        default_config = {'kinic_x': None, 'kinic_y': None, 'ai_response_x': None, 'ai_response_y': None}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    # Ensure all keys exist
                    for key in default_config:
                        if key not in self.config:
                            self.config[key] = default_config[key]
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
        
        # Main scrollable container
        main_container = tk.Frame(self.root, bg=COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_container, bg=COLORS['background'], highlightthickness=0)
        
        # Thick scrollbar
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", width=25, arrowsize=18)
        
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main = scrollable_frame
        
        # Setup section
        setup_frame = tk.LabelFrame(main, text="⚙️ Setup", 
                                   font=('Arial', 14, 'bold'),
                                   bg=COLORS['background'], padx=20, pady=15)
        setup_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        # Kinic position status
        if self.config.get('kinic_x'):
            pos_frame = tk.Frame(setup_frame, bg=COLORS['background'])
            pos_frame.pack(pady=5)
            tk.Label(pos_frame, text="✓ Kinic Position:", font=('Arial', 12), 
                    bg=COLORS['background'], fg=COLORS['success']).pack(side=tk.LEFT)
            tk.Label(pos_frame, text=f"({self.config['kinic_x']}, {self.config['kinic_y']})",
                    font=('Arial', 12), bg=COLORS['background']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(setup_frame, text="Setup Kinic Position", 
                 command=self.setup_kinic_position,
                 bg=COLORS['primary'], fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=10).pack(pady=5)
        
        # AI Response position status
        if self.config.get('ai_response_x'):
            ai_frame = tk.Frame(setup_frame, bg=COLORS['background'])
            ai_frame.pack(pady=5)
            tk.Label(ai_frame, text="✓ AI Response Position:", font=('Arial', 12),
                    bg=COLORS['background'], fg=COLORS['success']).pack(side=tk.LEFT)
            tk.Label(ai_frame, text=f"({self.config['ai_response_x']}, {self.config['ai_response_y']})",
                    font=('Arial', 12), bg=COLORS['background']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(setup_frame, text="Setup AI Response Position",
                 command=self.setup_ai_position,
                 bg=COLORS['primary'], fg='white', font=('Arial', 11),
                 padx=20, pady=8).pack(pady=5)
        
        # Actions section
        actions_frame = tk.LabelFrame(main, text="⚡ Actions",
                                     font=('Arial', 14, 'bold'),
                                     bg=COLORS['background'], padx=20, pady=15)
        actions_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        # Test Mouse Movement button
        tk.Button(actions_frame, text="🖱️ Test Mouse Movement",
                 command=self.test_mouse_action,
                 bg='#FFA500', fg='white',
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=8,
                 state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED).pack(pady=5)
        
        # Save Page button
        tk.Button(actions_frame, text="💾 Save Current Page",
                 command=self.save_page,
                 bg=COLORS['success'], fg='white',
                 font=('Arial', 12, 'bold'),
                 padx=30, pady=12,
                 state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED).pack(pady=5)
        
        # Search section
        search_frame = tk.Frame(actions_frame, bg=COLORS['background'])
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Search Query:",
                font=('Arial', 12),
                bg=COLORS['background']).pack(pady=5)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=40)
        self.search_entry.pack(pady=5)
        
        # Search and Retrieve URL button
        tk.Button(search_frame, text="🔗 Search & Retrieve First URL",
                 command=self.search_retrieve_url,
                 bg=COLORS['primary'], fg='white',
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=10,
                 state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED).pack(pady=5)
        
        # Extract URL from AI Response button
        tk.Button(search_frame, text="📋 Extract URL from AI Response",
                 command=self.extract_url_from_ai,
                 bg=COLORS['primary_dark'], fg='white',
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=10,
                 state=tk.NORMAL if PYAUTOGUI_AVAILABLE else tk.DISABLED).pack(pady=5)
        
        # Results section with scrollbar
        results_frame = tk.LabelFrame(main, text="📊 Results",
                                     font=('Arial', 14, 'bold'),
                                     bg=COLORS['background'], padx=20, pady=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_frame = tk.Frame(results_frame, bg=COLORS['background'])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_frame,
                                   height=15, width=80,
                                   font=('Consolas', 10),
                                   bg='#F8F9FA',
                                   wrap=tk.WORD)
        
        # Thick scrollbar for results
        results_scrollbar = tk.Scrollbar(text_frame,
                                        width=25,
                                        bg='#CBD5E1',
                                        activebackground='#94A3B8',
                                        troughcolor='#F1F5F9')
        
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        results_scrollbar.config(command=self.results_text.yview)
        
        self.log("Kinic Desktop ready!")
    
    def setup_kinic_position(self):
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showerror("Error", "pyautogui module not available!")
            return
        
        result = messagebox.showinfo("Setup Kinic Position",
            "1. Make sure Chrome is open with Kinic visible\n"
            "2. Click OK\n"
            "3. Move your mouse to the Kinic icon\n"
            "4. Keep it there for 5 seconds")
        
        self.log("Starting Kinic position setup...")
        
        # Countdown
        for i in range(5, 0, -1):
            self.log(f"Recording position in {i} seconds...")
            self.root.update()
            time.sleep(1)
        
        try:
            x, y = pyautogui.position()
            self.config['kinic_x'] = x
            self.config['kinic_y'] = y
            self.save_config()
            
            self.log(f"✅ Kinic position saved: ({x}, {y})")
            
            # Test click
            self.log("Testing click on Kinic icon...")
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            
            messagebox.showinfo("Success", f"Kinic position saved: ({x}, {y})")
            
            # Refresh UI
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_ui()
            
        except Exception as e:
            self.log(f"❌ Error setting position: {e}")
            messagebox.showerror("Error", f"Failed to set position: {e}")
    
    def setup_ai_position(self):
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showerror("Error", "pyautogui module not available!")
            return
        
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please setup Kinic position first!")
            return
        
        messagebox.showinfo("Setup AI Response Position",
            "1. I'll click on Kinic to open it\n"
            "2. When you see the AI response area, hover over it\n"
            "3. Keep your mouse there for 5 seconds")
        
        self.log("Opening Kinic...")
        pyautogui.click(self.config['kinic_x'], self.config['kinic_y'])
        time.sleep(2)
        
        self.log("Starting AI response position setup...")
        
        for i in range(5, 0, -1):
            self.log(f"Recording position in {i} seconds...")
            self.root.update()
            time.sleep(1)
        
        try:
            x, y = pyautogui.position()
            self.config['ai_response_x'] = x
            self.config['ai_response_y'] = y
            self.save_config()
            
            self.log(f"✅ AI response position saved: ({x}, {y})")
            messagebox.showinfo("Success", f"AI response position saved: ({x}, {y})")
            
            # Refresh UI
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_ui()
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
    
    def save_page(self):
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please setup Kinic position first!")
            return
        
        try:
            self.log("Saving current page...")
            
            # Get current position for debugging
            current_pos = pyautogui.position()
            self.log(f"Current mouse at: {current_pos}")
            
            # Press ESC to clear any popups
            self.log("Pressing ESC...")
            pyautogui.press('escape')
            time.sleep(1)
            
            # Move to Kinic icon
            target_x = self.config['kinic_x']
            target_y = self.config['kinic_y']
            self.log(f"Moving mouse to Kinic at ({target_x}, {target_y})...")
            
            # Force immediate movement
            pyautogui.moveTo(target_x, target_y, duration=0.5)
            self.root.update()  # Force GUI update
            
            # Verify movement
            new_pos = pyautogui.position()
            self.log(f"Mouse now at: {new_pos}")
            
            # Click
            self.log("Clicking...")
            pyautogui.click()
            time.sleep(0.8)
            
            # Navigate to save button (Shift+Tab then Enter)
            self.log("Pressing Shift+Tab...")
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.3)
            
            self.log("Pressing Enter...")
            pyautogui.press('enter')
            
            self.log("✅ Page save command sent!")
            
        except Exception as e:
            self.log(f"❌ Error saving page: {e}")
            import traceback
            self.log(traceback.format_exc())
    
    def search_retrieve_url(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please setup Kinic position first!")
            return
        
        def do_search():
            try:
                self.log(f"Searching for: {query}")
                
                # Clear and click Kinic
                pyautogui.press('escape')
                time.sleep(1)
                
                self.log(f"Clicking Kinic at ({self.config['kinic_x']}, {self.config['kinic_y']})")
                pyautogui.moveTo(self.config['kinic_x'], self.config['kinic_y'], duration=0.3)
                pyautogui.click()
                time.sleep(0.8)
                
                # Tab to search box (4 times)
                self.log("Navigating to search box...")
                for i in range(4):
                    pyautogui.press('tab')
                    time.sleep(0.2)
                
                # Type query and search
                self.log(f"Typing: {query}")
                pyautogui.typewrite(query)
                pyautogui.press('enter')
                
                # Wait for results
                self.log("Waiting for search results...")
                time.sleep(3)
                
                # Tab to first result
                self.log("Navigating to first result...")
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.press('tab')
                time.sleep(0.3)
                
                # Right-click menu
                self.log("Opening context menu...")
                pyautogui.hotkey('shift', 'f10')
                time.sleep(2)
                
                # Navigate to Copy Link
                self.log("Selecting 'Copy link address'...")
                for i in range(5):
                    pyautogui.press('down')
                    time.sleep(0.2)
                
                pyautogui.press('enter')
                time.sleep(0.5)
                
                # Get URL from clipboard
                if PYPERCLIP_AVAILABLE:
                    try:
                        url = pyperclip.paste()
                        self.log(f"✅ URL retrieved: {url}")
                    except:
                        self.log("✅ URL copied to clipboard")
                else:
                    self.log("✅ URL copied to clipboard")
                    
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        thread = threading.Thread(target=do_search)
        thread.daemon = True
        thread.start()
    
    def extract_url_from_ai(self):
        if not self.config.get('ai_response_x'):
            messagebox.showerror("Error", "Please setup AI response position first!")
            return
        
        def do_extract():
            try:
                self.log("Extracting URL from AI response...")
                
                # Triple-click to select all text in AI response
                self.log(f"Selecting text at ({self.config['ai_response_x']}, {self.config['ai_response_y']})")
                pyautogui.moveTo(self.config['ai_response_x'], self.config['ai_response_y'], duration=0.3)
                pyautogui.tripleClick()
                time.sleep(0.5)
                
                # Copy selected text
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.5)
                
                # Get text from clipboard
                if PYPERCLIP_AVAILABLE:
                    try:
                        text = pyperclip.paste()
                        # Simple URL extraction
                        import re
                        urls = re.findall(r'https?://[^\s]+', text)
                        if urls:
                            self.log(f"✅ Found {len(urls)} URL(s):")
                            for url in urls:
                                self.log(f"  - {url}")
                        else:
                            self.log("No URLs found in AI response")
                    except Exception as e:
                        self.log(f"Error reading clipboard: {e}")
                else:
                    self.log("✅ AI response copied to clipboard")
                    
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        thread = threading.Thread(target=do_extract)
        thread.daemon = True
        thread.start()
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def on_closing(self):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KinicDesktop()
    app.run()