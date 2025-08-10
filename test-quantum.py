#!/usr/bin/env python3
"""Test AI extraction with 'quantum computing' search"""

import requests
import time

print("="*60)
print("TESTING KINIC AI EXTRACTION")
print("="*60)
print("\nSearching for: quantum computing")
print("Expected time: ~56 seconds\n")

start = time.time()

try:
    response = requests.post(
        "http://localhost:5006/search-ai-extract",
        json={"query": "quantum computing"},
        timeout=120
    )
    
    elapsed = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"✅ API call successful ({elapsed:.1f}s)")
        
        ai_text = data.get('ai_response', '')
        
        # Check if we got real AI content
        if ai_text and len(ai_text) > 100:
            # Check if it's actually about quantum computing
            if "quantum" in ai_text.lower() or "qubit" in ai_text.lower():
                print(f"\n🎯 Got real AI response about quantum computing!")
                print(f"Length: {len(ai_text)} characters\n")
                print("First 500 characters:")
                print("-"*40)
                print(ai_text[:500])
                print("-"*40)
            else:
                print(f"\n⚠️ Got text but not about quantum computing")
                print(f"Length: {len(ai_text)} characters")
                print("Might be capturing wrong area. First 200 chars:")
                print(ai_text[:200])
        else:
            print(f"\n❌ Short or empty response: '{ai_text}'")
        
        # Save full response
        with open("quantum-response.txt", "w", encoding='utf-8') as f:
            f.write(ai_text)
        print("\n📄 Full response saved to quantum-response.txt")
        
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")