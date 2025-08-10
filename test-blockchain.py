#!/usr/bin/env python3
"""Test AI extraction with 'blockchain technology' search"""

import requests
import time

print("Testing AI extraction with 'blockchain technology' search...")
print("This will take about 56 seconds...\n")

start = time.time()

try:
    response = requests.post(
        "http://localhost:5006/search-ai-extract",
        json={"query": "blockchain technology"},
        timeout=120
    )
    
    elapsed = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"✅ Completed in {elapsed:.1f} seconds\n")
        print(f"Success: {data.get('success')}")
        print(f"Query: {data.get('query')}")
        
        ai_text = data.get('ai_response', '')
        print(f"\nAI Response ({len(ai_text)} characters):")
        print("="*60)
        print(ai_text)
        print("="*60)
        
        # Save to file
        with open("blockchain-ai-response.txt", "w") as f:
            f.write(f"Query: blockchain technology\n")
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Response length: {len(ai_text)} characters\n\n")
            f.write("AI Response:\n")
            f.write("="*60 + "\n")
            f.write(ai_text)
            f.write("\n" + "="*60)
        
        if len(ai_text) > 100:
            print("\n✅ SUCCESS! Got a proper AI response about blockchain")
            print("📄 Full response saved to blockchain-ai-response.txt")
        else:
            print("\n⚠️  Response seems short or might be a URL")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("❌ Request timed out after 120 seconds")
except Exception as e:
    print(f"❌ Error: {e}")