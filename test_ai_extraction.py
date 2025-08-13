#!/usr/bin/env python3
"""
Test script for Kinic /search-ai-extract endpoint
This will search saved content and extract AI analysis
"""

import requests
import time

def test_ai_extraction():
    """Test the /search-ai-extract endpoint"""
    
    print("="*60)
    print("TESTING KINIC /search-ai-extract ENDPOINT")
    print("="*60)
    
    # Test query
    test_query = "model accuracy and performance metrics"
    
    print(f"\n1. Testing AI extraction with query: '{test_query}'")
    print("   🔧 This will control your mouse and Chrome:")
    print("   • Focus Chrome browser")
    print("   • Close any popups (ESC)")
    print("   • Click Kinic extension button")
    print("   • Navigate to search field (TAB x4)")
    print("   • Type search query")
    print("   • Press ENTER to search")
    print("   • Navigate to AI button (TAB x5)")
    print("   • Click AI button (ENTER)")
    print("   • Wait for AI response (10 seconds)")
    print("   • Copy AI response to clipboard")
    print("   • Close Kinic (ESC)")
    
    print("\n🤖 WATCH YOUR SCREEN - Automation starting...")
    
    try:
        response = requests.post(
            "http://localhost:5006/search-ai-extract",
            json={"query": test_query}
        )
        result = response.json()
        
        print(f"\n📥 API RESPONSE:")
        print(f"   Success: {result.get('success')}")
        print(f"   Error: {result.get('error', 'None')}")
        
        if result.get('success'):
            ai_response = result.get('ai_response', '')
            query_used = result.get('query', '')
            sources_found = result.get('sources_found', 0)
            
            print(f"\n✅ SUCCESS: AI extraction completed!")
            print(f"   Query: {query_used}")
            print(f"   Sources found: {sources_found}")
            print(f"   Response length: {len(ai_response)} characters")
            print(f"\n🤖 AI RESPONSE:")
            print(f"   {ai_response}")
            
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"\n❌ FAILED: {error_msg}")
            
            if "powershell.exe" in error_msg or "clip.exe" in error_msg:
                print("\n💡 DIAGNOSIS: Clipboard access issue")
                print("   The automation worked but couldn't copy text from Windows clipboard")
                print("   Solutions:")
                print("   1. Run from Windows PowerShell instead of WSL")
                print("   2. Install WSL clipboard tools")
                print("   3. Use Ubuntu Desktop with proper display forwarding")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("   Make sure Kinic API is running: python kinic-api.py")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
    
    print("\n" + "="*60)
    print("AI EXTRACTION TEST COMPLETE")
    print("="*60)

def test_search_and_retrieve():
    """Test the /search-and-retrieve endpoint (simpler version)"""
    
    print("\n" + "="*60)
    print("TESTING KINIC /search-and-retrieve ENDPOINT")
    print("="*60)
    
    test_query = "sentiment analysis model"
    
    print(f"\nTesting search with query: '{test_query}'")
    print("This endpoint returns the first matching URL without AI analysis")
    
    try:
        response = requests.post(
            "http://localhost:5006/search-and-retrieve",
            json={"query": test_query}
        )
        result = response.json()
        
        print(f"\n📥 API RESPONSE:")
        print(f"   Success: {result.get('success')}")
        print(f"   Error: {result.get('error', 'None')}")
        
        if result.get('success'):
            found_url = result.get('url', '')
            query_used = result.get('query', '')
            
            print(f"\n✅ SUCCESS: Search completed!")
            print(f"   Query: {query_used}")
            print(f"   Found URL: {found_url}")
            
        else:
            print(f"\n❌ FAILED: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    test_ai_extraction()
    test_search_and_retrieve()