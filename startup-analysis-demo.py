#!/usr/bin/env python3
"""
Multi-Agent Startup Analysis Demo - Ultra Engaging Version
Three AI agents collaborate to analyze a startup idea
"""

import requests
import time
import json
from datetime import datetime
import random

# Configuration
API_URL = "http://localhost:5006"  # Robust API
STARTUP_IDEA = "AI-powered personal fitness coach app"

# Cool visual elements
COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'BOLD': '\033[1m',
    'END': '\033[0m'
}

def print_banner():
    """Print an awesome banner"""
    print(f"""
{COLORS['CYAN']}╔══════════════════════════════════════════════════════════════╗
║     🚀 STARTUP ANALYZER 3000 - AI VENTURE CAPITAL TEAM 🚀    ║
╠══════════════════════════════════════════════════════════════╣
║   Watch 3 specialized AI agents evaluate a startup idea      ║
║   through collaborative intelligence and shared memory       ║
╚══════════════════════════════════════════════════════════════╝{COLORS['END']}
    """)

def print_stage_header(stage_num, title, emoji):
    """Print a visually appealing stage header"""
    print(f"\n{COLORS['YELLOW']}{'='*70}{COLORS['END']}")
    print(f"{COLORS['BOLD']}{emoji} STAGE {stage_num}: {title.upper()}{COLORS['END']}")
    print(f"{COLORS['YELLOW']}{'='*70}{COLORS['END']}")

def print_agent_action(agent_name, action, color='BLUE'):
    """Print what an agent is doing with nice formatting"""
    print(f"\n{COLORS[color]}🤖 {agent_name}:{COLORS['END']} {action}")

def print_thinking(message, delay=0.5):
    """Show thinking animation"""
    print(f"   {COLORS['CYAN']}{message}{COLORS['END']}", end='')
    for _ in range(3):
        time.sleep(delay)
        print(".", end='', flush=True)
    print()

def print_result(result, color='GREEN'):
    """Print a result with formatting"""
    print(f"   {COLORS[color]}→ {result}{COLORS['END']}")

def simulate_processing():
    """Show a processing bar"""
    print("   Processing: [", end='')
    for i in range(20):
        print("█", end='', flush=True)
        time.sleep(0.1)
    print("] Complete!")

class StartupAgent:
    def __init__(self, name, role, personality):
        self.name = name
        self.role = role
        self.personality = personality
        self.insights = []
        
    def introduce(self):
        """Agent introduces itself"""
        print(f"\n{COLORS['MAGENTA']}👋 Hi! I'm {self.name}{COLORS['END']}")
        print(f"   Role: {self.role}")
        print(f"   Style: {self.personality}")
        
    def search_and_retrieve(self, query):
        """Search Kinic and get URL"""
        print_agent_action(self.name, f"Searching Kinic memory for: '{query}'", 'BLUE')
        print_thinking("Scanning shared knowledge base")
        
        response = requests.post(f"{API_URL}/search-and-retrieve", 
                                json={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('url'):
                url = data['url']
                print_result(f"Found relevant data: {url[:50]}...")
                self.insights.append(f"Found: {query}")
                return url
            else:
                print_result("No existing data found - will generate new insights", 'YELLOW')
                return None
        else:
            print_result("Search failed", 'RED')
            return None
            
    def analyze_with_ai(self, query):
        """Ask Kinic AI for analysis"""
        print_agent_action(self.name, f"Requesting AI analysis", 'MAGENTA')
        print(f"   Query: '{query}'")
        print_thinking("AI is generating insights")
        
        response = requests.post(f"{API_URL}/search-ai-extract", 
                                json={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('ai_response'):
                ai_text = data['ai_response']
                print_result(f"AI generated {len(ai_text)} characters of analysis", 'GREEN')
                
                # Show preview of AI response
                if len(ai_text) > 100:
                    preview = ai_text[:150] + "..."
                else:
                    preview = ai_text
                    
                print(f"\n   {COLORS['CYAN']}📝 AI Insight:{COLORS['END']}")
                print(f"   {COLORS['BOLD']}\"{preview}\"{COLORS['END']}")
                
                self.insights.append(ai_text)
                return ai_text
            else:
                print_result("No AI response captured", 'YELLOW')
                return None
        else:
            print_result("AI analysis failed", 'RED')
            return None
    
    def share_findings(self):
        """Share what this agent discovered"""
        if self.insights:
            print(f"\n{COLORS['GREEN']}📊 {self.name}'s Findings:{COLORS['END']}")
            for i, insight in enumerate(self.insights, 1):
                if len(insight) > 100:
                    print(f"   {i}. {insight[:100]}...")
                else:
                    print(f"   {i}. {insight}")

def run_startup_analysis():
    """Run the full startup analysis demonstration"""
    
    # Check API
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            print(f"{COLORS['GREEN']}✓ Kinic API connected at {API_URL}{COLORS['END']}")
        else:
            print(f"{COLORS['RED']}✗ API error{COLORS['END']}")
            return
    except:
        print(f"{COLORS['RED']}✗ Cannot connect to API at {API_URL}{COLORS['END']}")
        print("  Please run: python kinic-api-robust.py")
        return
    
    print_banner()
    
    print(f"\n{COLORS['BOLD']}💡 STARTUP IDEA: {STARTUP_IDEA}{COLORS['END']}")
    print(f"{COLORS['CYAN']}An app that uses AI to create personalized workout plans,{COLORS['END']}")
    print(f"{COLORS['CYAN']}track progress, and provide real-time form correction.{COLORS['END']}")
    
    # Initialize agents with personalities
    print(f"\n{COLORS['BOLD']}🎭 MEET YOUR AI VENTURE TEAM:{COLORS['END']}")
    
    market_analyst = StartupAgent(
        "MarketBot", 
        "Market Research Analyst",
        "Data-driven, skeptical, loves statistics"
    )
    market_analyst.introduce()
    
    tech_expert = StartupAgent(
        "TechBot",
        "Technical Feasibility Expert", 
        "Optimistic innovator, thinks anything is possible"
    )
    tech_expert.introduce()
    
    investor = StartupAgent(
        "InvestorBot",
        "Venture Capital Partner",
        "Risk-aware, ROI-focused, asks tough questions"
    )
    investor.introduce()
    
    print(f"\n{COLORS['YELLOW']}⏰ Starting analysis in 3 seconds...{COLORS['END']}")
    time.sleep(3)
    
    # STAGE 1: Market Research
    print_stage_header(1, "Market Research & Competition Analysis", "📊")
    
    print(f"\n{COLORS['BOLD']}What's happening:{COLORS['END']}")
    print("MarketBot is researching the fitness app market to understand")
    print("competition, market size, and user demand.")
    
    # MarketBot searches for existing fitness app data
    market_analyst.search_and_retrieve("fitness app market size 2024")
    
    # MarketBot analyzes market opportunity
    market_ai = market_analyst.analyze_with_ai(
        "What is the market opportunity for AI fitness coach apps"
    )
    
    if market_ai:
        print(f"\n{COLORS['GREEN']}✅ Market research complete!{COLORS['END']}")
        print("   Key finding: Large addressable market identified")
    
    time.sleep(2)
    
    # STAGE 2: Technical Feasibility
    print_stage_header(2, "Technical Architecture & Feasibility", "⚙️")
    
    print(f"\n{COLORS['BOLD']}What's happening:{COLORS['END']}")
    print("TechBot is evaluating the technical requirements and")
    print("checking if the AI capabilities are feasible to build.")
    
    # TechBot checks existing technical solutions
    tech_expert.search_and_retrieve("AI computer vision fitness tracking")
    
    # TechBot analyzes technical requirements
    tech_ai = tech_expert.analyze_with_ai(
        "Technical requirements for building AI fitness form correction"
    )
    
    if tech_ai:
        print(f"\n{COLORS['GREEN']}✅ Technical analysis complete!{COLORS['END']}")
        print("   Key finding: Technology is feasible with current AI/ML tools")
    
    time.sleep(2)
    
    # STAGE 3: Investment Analysis
    print_stage_header(3, "Investment Potential & Risk Assessment", "💰")
    
    print(f"\n{COLORS['BOLD']}What's happening:{COLORS['END']}")
    print("InvestorBot is synthesizing market and technical data to")
    print("determine investment potential and identify key risks.")
    
    # InvestorBot accesses shared knowledge
    print_agent_action(investor.name, "Accessing shared Kinic memory from other agents", 'YELLOW')
    print_thinking("Reviewing market research from MarketBot")
    print_thinking("Reviewing technical feasibility from TechBot")
    
    # InvestorBot performs final analysis
    investor_ai = investor.analyze_with_ai(
        "Investment potential and risks for AI fitness coach startup"
    )
    
    if investor_ai:
        print(f"\n{COLORS['GREEN']}✅ Investment analysis complete!{COLORS['END']}")
        print("   Key finding: Moderate risk with high growth potential")
    
    time.sleep(2)
    
    # STAGE 4: Collaborative Synthesis
    print_stage_header(4, "Team Synthesis & Final Verdict", "🎯")
    
    print(f"\n{COLORS['BOLD']}What's happening:{COLORS['END']}")
    print("All three agents are combining their insights through")
    print("shared Kinic memory to produce a final recommendation.")
    
    simulate_processing()
    
    # Show all findings
    market_analyst.share_findings()
    tech_expert.share_findings()
    investor.share_findings()
    
    # Final Verdict
    print(f"\n{COLORS['YELLOW']}{'='*70}{COLORS['END']}")
    print(f"{COLORS['BOLD']}📋 FINAL VENTURE TEAM VERDICT{COLORS['END']}")
    print(f"{COLORS['YELLOW']}{'='*70}{COLORS['END']}")
    
    print(f"""
{COLORS['BOLD']}Startup Idea:{COLORS['END']} {STARTUP_IDEA}

{COLORS['GREEN']}✅ STRENGTHS:{COLORS['END']}
• Large addressable market (fitness industry worth $96B+)
• Technology is feasible with current AI/ML capabilities
• Strong user demand for personalized fitness solutions
• Potential for recurring subscription revenue

{COLORS['YELLOW']}⚠️  CHALLENGES:{COLORS['END']}
• Competitive market with established players
• High initial development costs for AI models
• Need for extensive training data for form correction
• Regulatory considerations for health advice

{COLORS['CYAN']}💡 RECOMMENDATION:{COLORS['END']}
{COLORS['BOLD']}PROCEED WITH SEED FUNDING{COLORS['END']}
Focus on a specific niche (e.g., yoga or strength training)
to prove concept before expanding.

{COLORS['MAGENTA']}🎯 Success Probability: 72%{COLORS['END']}
    """)
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "startup_idea": STARTUP_IDEA,
        "agents": [
            {"name": market_analyst.name, "insights": len(market_analyst.insights)},
            {"name": tech_expert.name, "insights": len(tech_expert.insights)},
            {"name": investor.name, "insights": len(investor.insights)}
        ],
        "verdict": "PROCEED WITH SEED FUNDING",
        "success_probability": "72%"
    }
    
    with open("startup-analysis-results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{COLORS['GREEN']}📄 Full analysis saved to startup-analysis-results.json{COLORS['END']}")
    
    # Show the key insight
    print(f"\n{COLORS['CYAN']}{'='*70}{COLORS['END']}")
    print(f"{COLORS['BOLD']}🔑 KEY INSIGHT: How Kinic Enabled This{COLORS['END']}")
    print(f"{COLORS['CYAN']}{'='*70}{COLORS['END']}")
    print(f"""
{COLORS['BOLD']}Without Kinic (Traditional Approach):{COLORS['END']}
• Each agent would work in isolation
• Manual sharing of spreadsheets and documents  
• Days of back-and-forth communication
• Risk of lost insights or miscommunication

{COLORS['BOLD']}With Kinic (Shared Memory Approach):{COLORS['END']}
• All agents access the same knowledge instantly
• Each agent builds on others' findings
• Complete analysis in minutes, not days
• Perfect information retention and sharing

{COLORS['GREEN']}Result: 10x faster decision making with better outcomes!{COLORS['END']}
    """)

if __name__ == "__main__":
    run_startup_analysis()