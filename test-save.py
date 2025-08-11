#!/usr/bin/env python3
"""
Test the /save endpoint with proper timing
"""

import requests
import time
import webbrowser

KINIC_API = "http://localhost:5006"

print("\n" + "="*60)
print("TESTING SAVE FUNCTIONALITY")
print("="*60)

# Check API is running
try:
    response = requests.get(KINIC_API, timeout=5)
    if response.status_code == 200:
        config = response.json().get('config', {})
        print(f"\n✅ Kinic API is running")
        print(f"   Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    else:
        print(f"❌ API not responding properly")
        exit(1)
except Exception as e:
    print(f"❌ Cannot connect to API: {e}")
    print("Please run: python kinic-api.py")
    exit(1)

print("\n📋 Test Plan:")
print("1. Open a test webpage")
print("2. Call /save endpoint")
print("3. Verify the save completes")

# Open a test page
test_url = "https://example.com"
print(f"\n🌐 Opening test page: {test_url}")
webbrowser.open(test_url)

print("⏳ Waiting 5 seconds for page to load...")
time.sleep(5)

print("\n🔧 Calling /save endpoint...")
print("This will:")
print("  1. Focus Chrome")
print("  2. Press ESC to close any popup")
print("  3. Click Kinic button")
print("  4. Press SHIFT+TAB to navigate to Save")
print("  5. Press ENTER to save")
print("  6. Press ESC to close Kinic")

start_time = time.time()

try:
    response = requests.post(f"{KINIC_API}/save", timeout=30)
    elapsed = time.time() - start_time
    
    if response.json().get('success'):
        print(f"\n✅ Save completed successfully in {elapsed:.1f} seconds!")
        print("   The page should now be saved in Kinic")
    else:
        print(f"\n❌ Save failed after {elapsed:.1f} seconds")
        print(f"   Error: {response.json().get('message', 'Unknown error')}")
        
except requests.exceptions.Timeout:
    print("\n❌ Request timed out after 30 seconds")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*60)
print("To verify the save worked:")
print("1. Click the Kinic extension")
print("2. Search for 'example'")
print("3. You should see the saved page")
print("="*60)