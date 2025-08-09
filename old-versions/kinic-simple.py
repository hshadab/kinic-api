#!/usr/bin/env python3
"""Kinic Desktop - Simple Version with Direct Commands"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import json
import time
from datetime import datetime

COLORS = {
    'primary': '#6366F1',
    'success': '#10B981',
    'error': '#EF4444',
    'background': '#FFFFFF',
}

class KinicDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kinic Desktop - Simple")
        self.root.geometry("800x600")
        
        self.config_file = os.path.expanduser("~/.kinic/config.json")
        self.load_config()
        
        self.setup_ui()
    
    def load_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {'kinic_x': None, 'kinic_y': None}
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        # Title
        tk.Label(self.root, text="Kinic Desktop", 
                font=('Arial', 24, 'bold')).pack(pady=20)
        
        # Setup button
        tk.Button(self.root, text="Setup Kinic Position",
                 command=self.setup_position,
                 bg=COLORS['primary'], fg='white',
                 font=('Arial', 12), padx=20, pady=10).pack(pady=10)
        
        # Position display
        if self.config.get('kinic_x'):
            tk.Label(self.root, 
                    text=f"Position: ({self.config['kinic_x']}, {self.config['kinic_y']})",
                    font=('Arial', 11)).pack()
        
        # Test button
        tk.Button(self.root, text="Test Click at Position",
                 command=self.test_click,
                 bg=COLORS['success'], fg='white',
                 font=('Arial', 12), padx=20, pady=10).pack(pady=10)
        
        # Save page button
        tk.Button(self.root, text="Save Current Page",
                 command=self.save_page,
                 bg=COLORS['success'], fg='white',
                 font=('Arial', 12), padx=20, pady=10).pack(pady=10)
        
        # Output
        tk.Label(self.root, text="Output:", font=('Arial', 11)).pack(pady=5)
        self.output = tk.Text(self.root, height=15, width=70)
        self.output.pack(pady=10)
        
        self.log("Ready!")
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.output.see(tk.END)
        self.root.update()
    
    def setup_position(self):
        messagebox.showinfo("Setup",
            "1. Open Chrome with Kinic visible\n"
            "2. Note the position of the Kinic icon\n"
            "3. Click OK and enter the coordinates")
        
        # Simple dialog to enter coordinates
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Kinic Position")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Enter X coordinate:").pack(pady=5)
        x_entry = tk.Entry(dialog)
        x_entry.pack(pady=5)
        
        tk.Label(dialog, text="Enter Y coordinate:").pack(pady=5)
        y_entry = tk.Entry(dialog)
        y_entry.pack(pady=5)
        
        def save_pos():
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                self.config['kinic_x'] = x
                self.config['kinic_y'] = y
                self.save_config()
                self.log(f"Position saved: ({x}, {y})")
                dialog.destroy()
                
                # Refresh UI
                for widget in self.root.winfo_children():
                    widget.destroy()
                self.setup_ui()
            except:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        tk.Button(dialog, text="Save", command=save_pos,
                 bg=COLORS['primary'], fg='white').pack(pady=10)
    
    def test_click(self):
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please setup position first!")
            return
        
        x = self.config['kinic_x']
        y = self.config['kinic_y']
        
        self.log(f"Simulating click at ({x}, {y})")
        self.log("Check if Kinic opens!")
        
        # You would manually click at this position
        messagebox.showinfo("Manual Action Required",
            f"Please manually click at position ({x}, {y})\n"
            "This is where the Kinic icon should be.")
    
    def save_page(self):
        if not self.config.get('kinic_x'):
            messagebox.showerror("Error", "Please setup position first!")
            return
        
        x = self.config['kinic_x']
        y = self.config['kinic_y']
        
        self.log("To save the current page:")
        self.log(f"1. Click at position ({x}, {y}) to open Kinic")
        self.log("2. Press Shift+Tab")
        self.log("3. Press Enter")
        
        messagebox.showinfo("Manual Steps",
            f"1. Click at ({x}, {y}) to open Kinic\n"
            "2. Press Shift+Tab\n"
            "3. Press Enter")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KinicDesktop()
    app.run()