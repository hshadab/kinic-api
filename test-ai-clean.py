#!/usr/bin/env python3
"""Test AI extraction with clean clipboard"""

import requests
import subprocess
import time
from datetime import datetime

def clear_clipboard():
    """Clear the clipboard"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::Clear()
    """
    subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    print("✓ Clipboard cleared")

def get_clipboard():
    """Get clipboard content"""
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::GetText()
    """
    result = subprocess.run(
        ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
         "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True, text=True, timeout=5
    )
    return result.stdout.strip() if result.stdout else "[empty]"

print("""
╔════════════════════════════════════════════════╗
║   AI EXTRACTION TEST (CLEAN CLIPBOARD)        ║
╚════════════════════════════════════════════════╝
""")

# Clear clipboard first
print("Step 1: Clearing clipboard...")
clear_clipboard()
print(f"   Clipboard now: {get_clipboard()}")

# Test with a different query
query = "explain machine learning"

print(f"\nStep 2: Testing AI extraction for: '{query}'")
print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting...")

try:
    response = requests.post(
        "http://localhost:5006/search-ai-extract",
        json={"query": query},
        timeout=70
    )
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Complete!")
    
    if response.json().get('success'):
        ai_text = response.json().get('ai_response', '')
        
        print("\n✅ AI Response Extracted:")
        print("="*60)
        if ai_text:
            # Show first 300 chars
            print(ai_text[:300])
            if len(ai_text) > 300:
                print(f"\n... ({len(ai_text)} total characters)")
        else:
            print("[No text captured]")
        print("="*60)
        
        # Check clipboard after
        print(f"\nClipboard after extraction: {get_clipboard()[:100]}...")
        
    else:
        print(f"\n❌ Failed: {response.json()}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\nNote: Try clicking manually in the AI response area if text is wrong")