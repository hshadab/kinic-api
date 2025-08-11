#!/usr/bin/env python3
"""
Test AI extraction endpoint with correct coordinates
"""

import requests
import time
from datetime import datetime

KINIC_API = "http://localhost:5006"

print("\n" + "="*60)
print("TESTING AI EXTRACTION")
print("="*60)

# Check API status and configuration
try:
    response = requests.get(KINIC_API)
    if response.status_code == 200:
        config = response.json().get('config', {})
        print(f"\n✅ Kinic API is running at {KINIC_API}")
        print(f"Configuration:")
        print(f"  Kinic button: ({config.get('kinic_x', 'NOT SET')}, {config.get('kinic_y', 'NOT SET')})")
        print(f"  AI response: ({config.get('ai_response_x', 'NOT SET')}, {config.get('ai_response_y', 'NOT SET')})")
    else:
        print(f"❌ API returned status {response.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Cannot connect to API: {e}")
    print("Please run: python kinic-api.py")
    exit(1)

# Simple query
query = "legal"

print(f"\nQuery: '{query}'")
print("\nThis will:")
print("1. Open Kinic at position ({}, {})".format(config.get('kinic_x'), config.get('kinic_y')))
print("2. Search for '{}'".format(query))
print("3. Click AI button to generate response")
print("4. Extract text from position ({}, {})".format(config.get('ai_response_x'), config.get('ai_response_y')))
print("\nThis typically takes 30-40 seconds...")
print("-"*40)

start_time = time.time()

try:
    print(f"\nStarted at: {datetime.now().strftime('%H:%M:%S')}")
    print("Calling /search-ai-extract endpoint...")
    
    response = requests.post(
        f"{KINIC_API}/search-ai-extract",
        json={"query": query},
        timeout=120  # 2 minutes timeout
    )
    
    elapsed = time.time() - start_time
    print(f"Response received after {elapsed:.1f} seconds")
    
    result = response.json()
    
    print("\n" + "="*60)
    print("RESPONSE:")
    print("="*60)
    
    if result.get('success'):
        print(f"✅ SUCCESS!")
        print(f"\nQuery: {result.get('query')}")
        print(f"\nAI Response extracted: {len(result.get('ai_response', ''))} characters")
        
        ai_text = result.get('ai_response', '')
        if ai_text:
            print("\n--- AI Response Preview (first 500 chars) ---")
            preview = ai_text[:500] + "..." if len(ai_text) > 500 else ai_text
            print(preview)
            print("\n--- End of preview ---")
        else:
            print("⚠️  No AI response text captured")
    else:
        print(f"❌ FAILED")
        print(f"Message: {result.get('message', 'Unknown error')}")
        print(f"Full response: {result}")
    
except requests.exceptions.Timeout:
    print(f"\n❌ Request timed out after 120 seconds")
    print("The operation might still be running on the server")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print(f"\nTest completed at: {datetime.now().strftime('%H:%M:%S')}")
print("="*60)