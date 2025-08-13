#!/usr/bin/env python3
"""
Stripe API Documentation Multi-Agent Demo - Windows Native Version
Three agents demonstrating different Kinic capabilities with Stripe docs
Fixed: No duplicate actions, proper timing
"""

import requests
import time
import webbrowser
from datetime import datetime

# Configuration
KINIC_API = "http://localhost:5006"

# Pre-saved Stripe documentation URLs
STRIPE_URLS = {
    "payments": "https://stripe.com/docs/payments",
    "checkout": "https://stripe.com/docs/payments/checkout", 
    "api_reference": "https://stripe.com/docs/api"
}

def print_header():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        STRIPE API MULTI-AGENT DEMO WITH KINIC           ║
    ╠══════════════════════════════════════════════════════════╣
    ║  3 Agents demonstrating different Kinic capabilities:   ║
    ║  • Agent 1: Saves 3 Stripe documentation pages          ║
    ║  • Agent 2: Retrieves URL from saved content            ║
    ║  • Agent 3: Extracts AI insights from saved docs        ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def agent1_save_stripe_docs():
    """Agent 1: Documentation Collector - Saves multiple Stripe docs"""
    print("\n" + "="*60)
    print("🤖 AGENT 1: Documentation Collector")
    print("="*60)
    print("Mission: Save Stripe API documentation to Kinic memory")
    
    saved_count = 0
    
    # IMPORTANT: We need to manually navigate to each URL first
    # The /save endpoint saves the CURRENT page in Chrome
    for doc_type, url in STRIPE_URLS.items():
        print(f"\n📚 Processing {doc_type}:")
        print(f"   URL: {url}")
        
        # Open URL in Chrome
        print(f"   → Opening in Chrome...")
        webbrowser.open(url)
        
        # Wait for page to fully load
        print(f"   ⏳ Waiting 8 seconds for page to load...")
        time.sleep(8)
        
        # Now call the API to save the current page
        print(f"   → Calling Kinic API to save...")
        response = requests.post(f"{KINIC_API}/save", timeout=30)
        
        if response.json().get('success'):
            saved_count += 1
            print(f"   ✅ Saved {doc_type} documentation to Kinic")
        else:
            print(f"   ⚠️ Failed to save: {response.json().get('message', 'Unknown error')}")
        
        # Wait before processing next URL
        print(f"   ⏸️ Waiting 3 seconds before next document...")
        time.sleep(3)
    
    print(f"\n📊 Agent 1 Summary: Saved {saved_count}/{len(STRIPE_URLS)} Stripe documentation pages")
    return saved_count

def agent2_retrieve_url():
    """Agent 2: URL Retriever - Searches and retrieves a specific doc URL"""
    print("\n" + "="*60)
    print("🤖 AGENT 2: URL Retriever")
    print("="*60)
    print("Mission: Search Kinic memory and retrieve Checkout documentation URL")
    
    time.sleep(3)
    
    # Search for checkout documentation
    query = "stripe checkout"
    print(f"\n🔍 Searching for: '{query}'")
    print("   → This will open Kinic, search, and copy the first URL...")
    print("   ⏳ Expected time: 15-20 seconds...")
    
    start_time = time.time()
    response = requests.post(
        f"{KINIC_API}/search-and-retrieve",
        json={"query": query},
        timeout=60
    )
    elapsed = time.time() - start_time
    
    if response.json().get('success'):
        url = response.json().get('url', '')
        print(f"   ✅ Found URL in {elapsed:.1f} seconds: {url}")
        print(f"\n📊 Agent 2 Summary: Successfully retrieved Stripe Checkout URL from shared memory")
        return url
    else:
        print(f"   ⚠️ Could not retrieve URL after {elapsed:.1f} seconds")
        print(f"   Error: {response.json().get('message', 'Unknown error')}")
        return None

def agent3_extract_insights():
    """Agent 3: AI Analyst - Extracts insights from saved documentation"""
    print("\n" + "="*60)
    print("🤖 AGENT 3: AI Analyst")
    print("="*60)
    print("Mission: Extract AI insights about Stripe payment implementation")
    
    time.sleep(3)
    
    # Ask AI about Stripe implementation
    query = "explain how to implement Stripe payments with best practices"
    print(f"\n🧠 Asking AI: '{query}'")
    print("⏳ This will take 35-45 seconds:")
    print("   • Opening Kinic extension")
    print("   • Searching documentation")
    print("   • Clicking AI button")
    print("   • Waiting for AI generation")
    print("   • Extracting AI text")
    print("\n   Please be patient...")
    
    start_time = time.time()
    response = requests.post(
        f"{KINIC_API}/search-ai-extract",
        json={"query": query},
        timeout=120  # 2 minute timeout
    )
    elapsed = time.time() - start_time
    
    if response.json().get('success'):
        ai_response = response.json().get('ai_response', '')
        if ai_response:
            print(f"\n   ✅ AI Response received in {elapsed:.1f} seconds")
            print(f"   ✅ Extracted {len(ai_response)} characters")
            print("\n📝 AI Insights:")
            print("-" * 60)
            # Show first 500 characters or full response if shorter
            preview = ai_response[:500] + "..." if len(ai_response) > 500 else ai_response
            print(preview)
            print("-" * 60)
            print(f"\n📊 Agent 3 Summary: Successfully extracted AI insights")
            return ai_response
    else:
        print(f"   ⚠️ Could not extract AI insights after {elapsed:.1f} seconds")
        print(f"   Error: {response.json().get('message', 'Unknown error')}")
        return None

def main():
    """Run the complete multi-agent demonstration"""
    print_header()
    
    # Check if API is running
    print("\n🔍 Checking Kinic API status...")
    try:
        response = requests.get(KINIC_API, timeout=5)
        if response.status_code == 200:
            config = response.json().get('config', {})
            print(f"✅ Kinic API is running at {KINIC_API}")
            print(f"   Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
            print(f"   AI response: ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
        else:
            print(f"❌ API returned status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to Kinic API at {KINIC_API}")
        print(f"   Error: {e}")
        print("\n📌 To fix:")
        print("   1. Open PowerShell")
        print("   2. Navigate to kinic folder")
        print("   3. Run: python ../kinic-api.py")
        return
    
    print("\n⚠️ IMPORTANT: Make sure Chrome is open with Kinic extension visible")
    print("⏱️ This demo will take approximately 2-3 minutes to complete")
    input("\nPress Enter when ready to start the demonstration...")
    
    print("\n🎬 Starting automated demonstration...")
    print("Each agent will access the same Kinic shared memory")
    time.sleep(3)
    
    # Run Agent 1
    print("\n" + "─"*60)
    print("PHASE 1: DOCUMENT COLLECTION")
    print("─"*60)
    saved_docs = agent1_save_stripe_docs()
    
    if saved_docs == 0:
        print("\n⚠️ No documents were saved. Please check:")
        print("   • Chrome is open and active")
        print("   • Kinic extension is installed and visible")
        print("   • Coordinates are correct (run ../setup-tools/capture-mouse-windows.py)")
        return
    
    print("\n⏸️ Pausing 5 seconds before Agent 2...")
    time.sleep(5)
    
    # Run Agent 2
    print("\n" + "─"*60)
    print("PHASE 2: URL RETRIEVAL")
    print("─"*60)
    retrieved_url = agent2_retrieve_url()
    
    print("\n⏸️ Pausing 5 seconds before Agent 3...")
    time.sleep(5)
    
    # Run Agent 3
    print("\n" + "─"*60)
    print("PHASE 3: AI ANALYSIS")
    print("─"*60)
    ai_insights = agent3_extract_insights()
    
    # Final summary
    print("\n" + "="*60)
    print("🏁 DEMONSTRATION COMPLETE")
    print("="*60)
    
    success_count = sum([
        saved_docs > 0,
        retrieved_url is not None,
        ai_insights is not None
    ])
    
    print(f"""
    📊 FINAL RESULTS ({success_count}/3 successful):
    ------------------------------------------------
    • Agent 1: Saved {saved_docs} Stripe documentation pages {'✅' if saved_docs > 0 else '❌'}
    • Agent 2: Retrieved URL: {'✅ Success' if retrieved_url else '❌ Failed'}
    • Agent 3: AI Insights: {'✅ Extracted' if ai_insights else '❌ Failed'}
    
    💡 KEY TAKEAWAY:
    All three agents used different Kinic API capabilities while
    sharing the same on-chain memory. No direct communication or
    file transfers were needed between agents!
    
    🔗 Kinic Features Demonstrated:
    • /save - Save webpages to memory
    • /search-and-retrieve - Search and get URLs
    • /search-ai-extract - Get AI analysis of saved content
    
    🌐 Blockchain Advantage:
    The saved Stripe documentation is now permanently stored
    on-chain, accessible by any agent or user with Kinic!
    """)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"stripe_demo_results_{timestamp}.txt"
    
    with open(results_file, "w") as f:
        f.write(f"Stripe API Multi-Agent Demo Results\n")
        f.write(f"{'='*50}\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"API Endpoint: {KINIC_API}\n\n")
        f.write(f"Results:\n")
        f.write(f"--------\n")
        f.write(f"Agent 1 (Documentation Collector):\n")
        f.write(f"  • Saved {saved_docs} documents\n")
        for doc_type in STRIPE_URLS.keys():
            f.write(f"    - {doc_type}\n")
        f.write(f"\nAgent 2 (URL Retriever):\n")
        f.write(f"  • Query: 'stripe checkout'\n")
        f.write(f"  • Retrieved URL: {retrieved_url or 'None'}\n")
        f.write(f"\nAgent 3 (AI Analyst):\n")
        f.write(f"  • Query: 'explain how to implement Stripe payments with best practices'\n")
        f.write(f"  • AI Response: {len(ai_insights) if ai_insights else 0} characters\n")
        if ai_insights:
            f.write(f"\nFull AI Response:\n")
            f.write(f"{'-'*50}\n")
            f.write(f"{ai_insights}\n")
    
    print(f"\n📄 Results saved to: {results_file}")
    
    # Offer to open results
    print("\n🎯 Next Steps:")
    print("   1. Review the saved results file")
    print("   2. Try searching Kinic manually for 'stripe'")
    print("   3. Run the demo again with different queries")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please check that the Kinic API is running correctly")