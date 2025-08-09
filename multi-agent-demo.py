#!/usr/bin/env python3
"""
Multi-Agent Kinic Demo - Research Team
Three AI agents collaborating through shared Kinic memory
"""

import requests
import time
import json
from datetime import datetime

# Configuration
KINIC_API = "http://localhost:5005"
RESEARCH_TOPIC = "quantum computing"

class KinicAgent:
    """Base class for all agents using Kinic"""
    
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.memory_api = KINIC_API
        
    def save_to_memory(self, note=""):
        """Save current page to shared memory"""
        response = requests.post(f"{self.memory_api}/save")
        print(f"[{self.name}] Saved to Kinic: {note}")
        return response.json()
    
    def search_memory(self, query):
        """Search shared memory"""
        response = requests.post(
            f"{self.memory_api}/search-and-retrieve",
            json={"query": query}
        )
        return response.json()
    
    def analyze_memory(self, query):
        """Get AI analysis from shared memory"""
        response = requests.post(
            f"{self.memory_api}/search-ai-extract",
            json={"query": query}
        )
        return response.json()
    
    def log_action(self, action):
        """Log agent actions for demo visibility"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] {self.name} ({self.role})")
        print(f"→ {action}")
        print("-" * 50)


class ResearchAgent(KinicAgent):
    """Agent 1: Finds and saves research materials"""
    
    def __init__(self):
        super().__init__("ResearchBot", "Research Collector")
    
    def collect_research(self, urls):
        """Simulate collecting research URLs"""
        self.log_action(f"Starting research collection on: {RESEARCH_TOPIC}")
        
        for url in urls:
            print(f"\n📚 Visiting: {url}")
            # In real usage, you'd navigate to URL first
            # For demo, we simulate with instructions
            input(f"   [Manual Step] Please navigate to {url} in Chrome, then press Enter...")
            
            self.save_to_memory(f"Research article: {url}")
            time.sleep(2)
        
        self.log_action(f"Collected {len(urls)} research sources")
        return len(urls)


class AnalysisAgent(KinicAgent):
    """Agent 2: Analyzes saved content"""
    
    def __init__(self):
        super().__init__("AnalysisBot", "Content Analyzer")
    
    def analyze_topic(self, topic):
        """Analyze all saved content about a topic"""
        self.log_action(f"Analyzing saved content about: {topic}")
        
        # Search for content
        search_result = self.search_memory(topic)
        if search_result.get('success'):
            print(f"✓ Found relevant content: {search_result.get('url', 'Multiple sources')}")
        
        # Get AI analysis
        analysis = self.analyze_memory(f"explain the key concepts from {topic} articles")
        
        if analysis.get('success'):
            self.log_action("Analysis complete")
            return analysis.get('ai_response', 'No analysis available')
        return None


class SummaryAgent(KinicAgent):
    """Agent 3: Creates final summary from collective knowledge"""
    
    def __init__(self):
        super().__init__("SummaryBot", "Report Writer")
        self.findings = []
    
    def gather_insights(self, queries):
        """Gather insights from shared memory"""
        self.log_action("Gathering insights from team's research")
        
        for query in queries:
            print(f"\n🔍 Checking: {query}")
            result = self.analyze_memory(query)
            if result.get('success'):
                self.findings.append({
                    'query': query,
                    'insight': result.get('ai_response', '')[:200] + "..."
                })
                print(f"   ✓ Found insights")
        
        return self.findings
    
    def create_report(self):
        """Create final report from all findings"""
        self.log_action("Creating final report from collective knowledge")
        
        report = f"""
        MULTI-AGENT RESEARCH REPORT
        ============================
        Topic: {RESEARCH_TOPIC}
        Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        Agents: ResearchBot, AnalysisBot, SummaryBot
        
        KEY FINDINGS:
        """
        
        for i, finding in enumerate(self.findings, 1):
            report += f"\n{i}. {finding['query'].upper()}\n"
            report += f"   {finding['insight']}\n"
        
        report += f"\n[Report compiled from {len(self.findings)} shared memory queries]"
        return report


def run_demo():
    """Run the multi-agent demonstration"""
    
    print("""
    ╔══════════════════════════════════════════════════╗
    ║     KINIC MULTI-AGENT DEMO - RESEARCH TEAM      ║
    ╠══════════════════════════════════════════════════╣
    ║  Watch 3 AI agents collaborate through shared   ║
    ║  Kinic memory to research and analyze a topic   ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # Initialize agents
    researcher = ResearchAgent()
    analyst = AnalysisAgent()
    summarizer = SummaryAgent()
    
    print(f"\n🎯 Research Topic: {RESEARCH_TOPIC}")
    print("\n👥 Agents initialized:")
    print(f"   • {researcher.name} - {researcher.role}")
    print(f"   • {analyst.name} - {analyst.role}")
    print(f"   • {summarizer.name} - {summarizer.role}")
    
    input("\nPress Enter to start the demonstration...")
    
    # Phase 1: Research Collection
    print("\n" + "="*60)
    print("PHASE 1: RESEARCH COLLECTION")
    print("="*60)
    
    research_urls = [
        "https://en.wikipedia.org/wiki/Quantum_computing",
        "https://www.ibm.com/quantum/what-is-quantum-computing",
        # Add more URLs as needed
    ]
    
    researcher.collect_research(research_urls)
    
    # Phase 2: Content Analysis
    print("\n" + "="*60)
    print("PHASE 2: CONTENT ANALYSIS")
    print("="*60)
    
    time.sleep(2)
    analysis = analyst.analyze_topic(RESEARCH_TOPIC)
    if analysis:
        print(f"\n📊 Analysis Preview:\n{analysis[:300]}...")
    
    # Phase 3: Report Generation
    print("\n" + "="*60)
    print("PHASE 3: REPORT GENERATION")
    print("="*60)
    
    time.sleep(2)
    insight_queries = [
        f"what are the basics of {RESEARCH_TOPIC}",
        f"what are the applications of {RESEARCH_TOPIC}",
        f"what are the challenges in {RESEARCH_TOPIC}"
    ]
    
    summarizer.gather_insights(insight_queries)
    final_report = summarizer.create_report()
    
    # Display final report
    print("\n" + "="*60)
    print("FINAL COLLABORATIVE REPORT")
    print("="*60)
    print(final_report)
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60)
    print("""
    This demonstration showed how multiple agents can:
    • Share a common knowledge base through Kinic
    • Build on each other's work
    • Collaborate without direct communication
    • Create collective intelligence
    
    The same Kinic memory can be accessed by ANY agent or tool!
    """)


if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(KINIC_API)
        print(f"✓ Kinic API is running at {KINIC_API}")
    except:
        print(f"❌ Please start the Kinic API first: python kinic-api.py")
        exit(1)
    
    run_demo()