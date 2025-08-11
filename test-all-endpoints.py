#!/usr/bin/env python3
"""
Test all three main endpoints with proper Chrome focus and ESC steps
"""

import requests
import time
import webbrowser
from datetime import datetime

KINIC_API = "http://localhost:5006"

def print_header():
    print("\n" + "="*60)
    print("TESTING ALL KINIC ENDPOINTS")
    print("="*60)
    print("\nAll endpoints follow the same pattern:")
    print("  1. Focus Chrome (click safe area)")
    print("  2. ESC to close any existing popup")
    print("  3. Open Kinic")
    print("  4. Perform action")
    print("  5. ESC to close Kinic")

def check_api():
    """Check if API is running"""
    try:
        response = requests.get(KINIC_API, timeout=5)
        if response.status_code == 200:
            config = response.json().get('config', {})
            print(f"\n✅ Kinic API is running")
            print(f"   Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
            print(f"   AI response: ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
            return True
    except:
        pass
    
    print(f"\n❌ Cannot connect to API")
    print("Please run: python kinic-api.py")
    return False

def test_save():
    """Test /save endpoint"""
    print("\n" + "-"*60)
    print("TEST 1: SAVE ENDPOINT")
    print("-"*60)
    
    # Open a test page
    test_url = "https://example.com"
    print(f"Opening test page: {test_url}")
    webbrowser.open(test_url)
    time.sleep(5)
    
    print("Calling /save endpoint...")
    start_time = time.time()
    
    try:
        response = requests.post(f"{KINIC_API}/save", timeout=30)
        elapsed = time.time() - start_time
        
        if response.json().get('success'):
            print(f"✅ Save completed in {elapsed:.1f} seconds")
            return True
        else:
            print(f"❌ Save failed: {response.json().get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search_and_retrieve():
    """Test /search-and-retrieve endpoint"""
    print("\n" + "-"*60)
    print("TEST 2: SEARCH AND RETRIEVE ENDPOINT")
    print("-"*60)
    
    query = "example"
    print(f"Searching for: '{query}'")
    print("Calling /search-and-retrieve endpoint...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{KINIC_API}/search-and-retrieve",
            json={"query": query},
            timeout=60
        )
        elapsed = time.time() - start_time
        
        if response.json().get('success'):
            url = response.json().get('url', '')
            print(f"✅ Retrieved URL in {elapsed:.1f} seconds")
            print(f"   URL: {url[:80]}..." if len(url) > 80 else f"   URL: {url}")
            return True
        else:
            print(f"❌ Search failed: {response.json().get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ai_extraction():
    """Test /search-ai-extract endpoint"""
    print("\n" + "-"*60)
    print("TEST 3: AI EXTRACTION ENDPOINT")
    print("-"*60)
    
    query = "what is example.com"
    print(f"AI Query: '{query}'")
    print("Calling /search-ai-extract endpoint...")
    print("(This takes 35-45 seconds)")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{KINIC_API}/search-ai-extract",
            json={"query": query},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.json().get('success'):
            ai_response = response.json().get('ai_response', '')
            print(f"✅ AI extraction completed in {elapsed:.1f} seconds")
            print(f"   Extracted {len(ai_response)} characters")
            if ai_response:
                preview = ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
                print(f"   Preview: {preview}")
            return True
        else:
            print(f"❌ AI extraction failed: {response.json().get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print_header()
    
    if not check_api():
        return
    
    print("\n⚠️ Make sure Chrome is open with Kinic extension visible")
    input("Press Enter to start tests...")
    
    results = {
        "save": False,
        "search": False,
        "ai": False
    }
    
    # Test 1: Save
    print("\n🧪 Starting Test 1...")
    results["save"] = test_save()
    time.sleep(3)
    
    # Test 2: Search and Retrieve
    print("\n🧪 Starting Test 2...")
    results["search"] = test_search_and_retrieve()
    time.sleep(3)
    
    # Test 3: AI Extraction
    print("\n🧪 Starting Test 3...")
    results["ai"] = test_ai_extraction()
    
    # Summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    print(f"  • Save endpoint:     {'✅ PASS' if results['save'] else '❌ FAIL'}")
    print(f"  • Search endpoint:   {'✅ PASS' if results['search'] else '❌ FAIL'}")
    print(f"  • AI extract:        {'✅ PASS' if results['ai'] else '❌ FAIL'}")
    
    if passed == total:
        print("\n🎉 All tests passed! All endpoints properly:")
        print("   1. Focus Chrome")
        print("   2. Close existing popups (ESC)")
        print("   3. Open Kinic")
        print("   4. Perform their action")
        print("   5. Close Kinic (ESC)")
    else:
        print("\n⚠️ Some tests failed. Check the API console for details.")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"test_results_{timestamp}.txt", "w") as f:
        f.write("Kinic API Test Results\n")
        f.write(f"Timestamp: {datetime.now()}\n\n")
        f.write(f"Results:\n")
        f.write(f"  Save: {'PASS' if results['save'] else 'FAIL'}\n")
        f.write(f"  Search: {'PASS' if results['search'] else 'FAIL'}\n")
        f.write(f"  AI Extract: {'PASS' if results['ai'] else 'FAIL'}\n")
    
    print(f"\n📄 Results saved to test_results_{timestamp}.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")