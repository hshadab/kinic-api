#!/usr/bin/env python3
"""Test AI response extraction with robust API"""

import requests
import time
from datetime import datetime

def log_time(message):
    """Print with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

print("""
╔════════════════════════════════════════════════╗
║      TEST AI RESPONSE EXTRACTION              ║
╚════════════════════════════════════════════════╝

This will:
1. Search for "Python tutorial" in Kinic
2. Click the AI button
3. Wait for AI to generate response
4. Extract the AI text

Expected time: ~38 seconds
""")

# Test query
query = "Python programming basics"

log_time(f"Starting AI extraction for: '{query}'")
log_time("This will take about 38 seconds with proper timing...")

print("\nCalling API...")
start_time = time.time()

try:
    response = requests.post(
        "http://localhost:5006/search-ai-extract",
        json={"query": query},
        timeout=60
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    log_time(f"Completed in {duration:.1f} seconds")
    
    if response.json().get('success'):
        print("\n✅ SUCCESS! AI Response Extracted:")
        print("="*50)
        ai_text = response.json().get('ai_response', 'No text captured')
        
        # Print first 500 characters of AI response
        if ai_text and len(ai_text) > 0:
            print(ai_text[:500])
            if len(ai_text) > 500:
                print(f"\n... (Total: {len(ai_text)} characters)")
        else:
            print("No AI response captured")
            
        print("="*50)
        print(f"\n📊 Stats:")
        print(f"   Query: {query}")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Response length: {len(ai_text) if ai_text else 0} characters")
    else:
        print(f"\n❌ Failed: {response.json()}")
        
except requests.exceptions.Timeout:
    print("\n❌ Request timed out (took longer than 60 seconds)")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*50)
print("Note: Kinic should have closed automatically")