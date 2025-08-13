#!/usr/bin/env python3
"""
Test script for Kinic /save endpoint
This will open a page and save it to Kinic's vector database
"""

import requests
import webbrowser
import time

def test_save():
    """Test the /save endpoint with a real page"""
    
    print("="*60)
    print("TESTING KINIC /save ENDPOINT")
    print("="*60)
    
    # Test page to save
    test_url = "https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    print(f"\n1. Opening test page: {test_url}")
    webbrowser.open(test_url)
    
    print("2. Waiting 5 seconds for page to fully load...")
    time.sleep(5)
    
    print("3. Calling Kinic /save API...")
    print("   🔧 This will control your mouse and Chrome:")
    print("   • Focus Chrome browser")
    print("   • Close any popups (ESC)")
    print("   • Click Kinic extension button")
    print("   • Navigate to save button (SHIFT+TAB)")
    print("   • Press ENTER to save")
    print("   • Close Kinic (ESC)")
    
    print("\n🤖 WATCH YOUR SCREEN - Automation starting...")
    
    try:
        response = requests.post("http://localhost:5006/save")
        result = response.json()
        
        print(f"\n📥 API RESPONSE:")
        print(f"   Success: {result.get('success')}")
        print(f"   Message: {result.get('message')}")
        print(f"   Error: {result.get('error', 'None')}")
        
        if result.get('success'):
            print("\n✅ SUCCESS: Page saved to Kinic vector database!")
            print("   The sentiment model page is now searchable via semantic queries")
        else:
            print(f"\n❌ FAILED: {result.get('error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("   Make sure Kinic API is running: python kinic-api.py")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
    
    print("\n" + "="*60)
    print("SAVE TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_save()