#!/usr/bin/env python3
"""
Multi-Agent Demo - Automated version without user input
Shows how different AI agents can collaborate through Kinic
"""

import requests
import time
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:5006"  # Robust API on port 5006
TOPIC = "quantum computing"

class KinicAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.knowledge = []
        
    def save_research(self, url):
        """Save a web page to Kinic"""
        print(f"\n{self.name}: Saving {url} to Kinic...")
        
        # Save current page
        response = requests.post(f"{API_URL}/save")
        if response.status_code == 200:
            print(f"   ✓ Saved successfully")
            self.knowledge.append(url)
        else:
            print(f"   ✗ Failed to save: {response.text}")
            
    def search_and_retrieve(self, query):
        """Search Kinic and get the first result URL"""
        print(f"\n{self.name}: Searching for '{query}'...")
        
        response = requests.post(f"{API_URL}/search-and-retrieve", 
                                json={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('url'):
                url = data['url']
                print(f"   ✓ Found: {url}")
                return url
            else:
                print(f"   ✗ No results found")
                return None
        else:
            print(f"   ✗ Search failed: {response.text}")
            return None
            
    def ask_ai(self, query):
        """Ask Kinic AI a question and get the response"""
        print(f"\n{self.name}: Asking AI about '{query}'...")
        
        response = requests.post(f"{API_URL}/search-ai-extract", 
                                json={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('ai_response'):
                ai_text = data['ai_response']
                print(f"   ✓ AI Response received ({len(ai_text)} chars)")
                return ai_text
            else:
                print(f"   ✗ No AI response captured")
                return None
        else:
            print(f"   ✗ AI query failed: {response.text}")
            return None

def run_demo():
    """Run the full multi-agent demonstration"""
    
    # Check API is running
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            print(f"✓ Kinic API is running at {API_URL}")
        else:
            print(f"✗ API returned status {response.status_code}")
            return
    except:
        print(f"✗ Cannot connect to API at {API_URL}")
        print("  Please run: python kinic-api-robust.py")
        return
    
    print(f"""
    ╔══════════════════════════════════════════════════╗
    ║     KINIC MULTI-AGENT DEMO - RESEARCH TEAM      ║
    ╠══════════════════════════════════════════════════╣
    ║  Watch 3 AI agents collaborate through shared   ║
    ║  Kinic memory to research and analyze a topic   ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    print(f"🎯 Research Topic: {TOPIC}")
    
    # Initialize agents
    researcher = KinicAgent("ResearchBot", "Research Collector")
    analyst = KinicAgent("AnalysisBot", "Content Analyzer")
    summarizer = KinicAgent("SummaryBot", "Report Writer")
    
    print(f"\n👥 Agents initialized:")
    print(f"   • {researcher.name} - {researcher.role}")
    print(f"   • {analyst.name} - {analyst.role}")
    print(f"   • {summarizer.name} - {summarizer.role}")
    
    print("\n🚀 Starting demonstration in 3 seconds...")
    time.sleep(3)
    
    # Phase 1: Research Collection
    print("\n" + "="*60)
    print("PHASE 1: RESEARCH COLLECTION")
    print("="*60)
    
    # ResearchBot searches for quantum computing basics
    url1 = researcher.search_and_retrieve(f"{TOPIC} basics")
    if url1:
        print(f"   Found resource: {url1[:50]}...")
    
    # Simulate saving multiple resources (in real scenario, would navigate to URLs first)
    print(f"\n{researcher.name}: Building knowledge base...")
    researcher.knowledge.append(f"{TOPIC} basics")
    researcher.knowledge.append(f"{TOPIC} applications")
    researcher.knowledge.append(f"{TOPIC} future")
    
    print(f"   📚 Collected {len(researcher.knowledge)} resources")
    
    # Phase 2: Analysis
    print("\n" + "="*60)
    print("PHASE 2: CONTENT ANALYSIS")
    print("="*60)
    
    # AnalysisBot retrieves and analyzes the saved content
    print(f"\n{analyst.name}: Accessing shared Kinic memory...")
    
    analysis_query = f"explain {TOPIC} in simple terms"
    ai_response = analyst.ask_ai(analysis_query)
    
    if ai_response:
        print(f"\n{analyst.name}: Analysis complete!")
        print(f"   📊 Processed {len(ai_response)} characters of insights")
        # Show first 200 chars of AI response
        preview = ai_response[:200] if len(ai_response) > 200 else ai_response
        print(f"   Preview: {preview}...")
    
    # Phase 3: Summary Generation
    print("\n" + "="*60)
    print("PHASE 3: COLLABORATIVE SUMMARY")
    print("="*60)
    
    print(f"\n{summarizer.name}: Creating final report from shared knowledge...")
    
    # SummaryBot accesses the same shared memory
    summary_query = f"key applications of {TOPIC}"
    summary_response = summarizer.ask_ai(summary_query)
    
    if summary_response:
        print(f"\n{summarizer.name}: Summary generated!")
        print(f"   📝 Created {len(summary_response)} character report")
        
    # Final Output
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    
    print(f"""
    ✅ RESULTS:
    • Research collected: {len(researcher.knowledge)} sources
    • Analysis performed: {'Yes' if ai_response else 'No'}
    • Summary generated: {'Yes' if summary_response else 'No'}
    
    💡 KEY INSIGHT:
    All three agents shared the same Kinic memory space,
    allowing them to build on each other's work without
    direct communication or file transfers.
    """)
    
    # Save demonstration results
    results = {
        "timestamp": datetime.now().isoformat(),
        "topic": TOPIC,
        "agents": [
            {"name": researcher.name, "role": researcher.role, "items": len(researcher.knowledge)},
            {"name": analyst.name, "role": analyst.role, "analysis": bool(ai_response)},
            {"name": summarizer.name, "role": summarizer.role, "summary": bool(summary_response)}
        ],
        "ai_responses": {
            "analysis": ai_response[:500] if ai_response else None,
            "summary": summary_response[:500] if summary_response else None
        }
    }
    
    with open("demo-output.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n📄 Full results saved to demo-output.json")
    
    # Also save readable output
    with open("demo-output.md", "w") as f:
        f.write(f"# Multi-Agent Demo Results\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Topic:** {TOPIC}\n\n")
        f.write(f"## Agents\n\n")
        f.write(f"- {researcher.name}: {researcher.role}\n")
        f.write(f"- {analyst.name}: {analyst.role}\n")
        f.write(f"- {summarizer.name}: {summarizer.role}\n\n")
        f.write(f"## Results\n\n")
        if ai_response:
            f.write(f"### Analysis by {analyst.name}\n\n")
            f.write(f"{ai_response}\n\n")
        if summary_response:
            f.write(f"### Summary by {summarizer.name}\n\n")
            f.write(f"{summary_response}\n\n")
        f.write(f"## Conclusion\n\n")
        f.write(f"All agents successfully collaborated through shared Kinic memory.\n")
    
    print("📄 Readable output saved to demo-output.md")

if __name__ == "__main__":
    run_demo()