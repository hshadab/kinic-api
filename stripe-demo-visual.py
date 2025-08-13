#!/usr/bin/env python3
"""
Stripe API Multi-Agent Demo - Visual Marketing Version
Live display of inputs/outputs - perfect for demos and recordings
"""

import requests
import time
import webbrowser
from datetime import datetime
import sys
import os

# Configuration
KINIC_API = "http://localhost:5006"

# Pre-saved Stripe documentation URLs
STRIPE_URLS = {
    "payments": "https://stripe.com/docs/payments",
    "checkout": "https://stripe.com/docs/payments/checkout", 
    "api_reference": "https://stripe.com/docs/api"
}

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color=Colors.END):
    """Print with color"""
    print(f"{color}{text}{Colors.END}")

def type_effect(text, delay=0.03, color=Colors.GREEN):
    """Typewriter effect for dramatic display"""
    print(color, end='')
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(Colors.END)

def print_box(title, content, color=Colors.CYAN):
    """Print content in a nice box"""
    width = max(len(title) + 4, max([len(line) for line in content.split('\n')] + [0]) + 4)
    print(color)
    print("╔" + "═" * width + "╗")
    print(f"║ {title.center(width-2)} ║")
    print("╠" + "═" * width + "╣")
    for line in content.split('\n'):
        if line:
            print(f"║ {line.ljust(width-2)} ║")
    print("╚" + "═" * width + "╝")
    print(Colors.END)

def countdown(seconds, message="Starting in"):
    """Visual countdown"""
    for i in range(seconds, 0, -1):
        print(f"\r{Colors.YELLOW}⏱️  {message} {i}...{Colors.END}", end='', flush=True)
        time.sleep(1)
    print("\r" + " " * 50 + "\r", end='')  # Clear line

def loading_animation(duration, message="Processing"):
    """Show loading animation"""
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.YELLOW}{symbols[i % len(symbols)]} {message}...{Colors.END}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 50 + "\r", end='')  # Clear line

def print_header():
    clear_screen()
    print_colored("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║     🚀 KINIC + STRIPE: MULTI-AGENT AI COLLABORATION DEMO 🚀        ║
    ║                                                                      ║
    ║      Witness 3 AI Agents Share Knowledge Through Blockchain         ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """, Colors.HEADER + Colors.BOLD)

def display_agent_card(agent_num, name, role, mission):
    """Display agent introduction card"""
    print()
    print_colored(f"    {'━' * 60}", Colors.BLUE)
    print_colored(f"    AGENT {agent_num}", Colors.BOLD + Colors.BLUE)
    print_colored(f"    {name}", Colors.BOLD + Colors.CYAN)
    print_colored(f"    Role: {role}", Colors.CYAN)
    print_colored(f"    Mission: {mission}", Colors.GREEN)
    print_colored(f"    {'━' * 60}", Colors.BLUE)
    print()

def show_live_input(label, value, color=Colors.YELLOW):
    """Show input being sent"""
    print(f"\n{Colors.BOLD}📥 INPUT:{Colors.END}")
    print(f"   {label}: {color}{value}{Colors.END}")

def show_live_output(label, value, success=True):
    """Show output received"""
    icon = "✅" if success else "❌"
    color = Colors.GREEN if success else Colors.RED
    print(f"\n{Colors.BOLD}📤 OUTPUT:{Colors.END}")
    print(f"   {icon} {label}: {color}{value}{Colors.END}")

def agent1_save_stripe_docs():
    """Agent 1: Documentation Collector - Saves multiple Stripe docs"""
    display_agent_card(
        1,
        "📚 Documentation Collector",
        "Senior Knowledge Curator",
        "Save critical Stripe API documentation to blockchain memory"
    )
    
    saved_count = 0
    results = []
    
    for doc_type, url in STRIPE_URLS.items():
        print(f"\n{Colors.BOLD}[{doc_type.upper()}]{Colors.END}")
        show_live_input("URL", url[:50] + "...")
        
        # Open URL in Chrome
        type_effect(f"→ Opening {doc_type} documentation in Chrome...", 0.02)
        webbrowser.open(url)
        
        loading_animation(8, f"Waiting for {doc_type} page to load")
        
        # Call API to save
        type_effect(f"→ Saving to Kinic blockchain memory...", 0.02)
        
        start_time = time.time()
        response = requests.post(f"{KINIC_API}/save", timeout=30)
        elapsed = time.time() - start_time
        
        if response.json().get('success'):
            saved_count += 1
            show_live_output(f"Saved {doc_type}", f"Success in {elapsed:.1f}s", True)
            results.append(f"✅ {doc_type}")
        else:
            show_live_output(f"Save {doc_type}", "Failed", False)
            results.append(f"❌ {doc_type}")
        
        time.sleep(2)
    
    # Agent summary
    print_box(
        f"AGENT 1 RESULTS",
        f"Documents Saved: {saved_count}/3\n" + "\n".join(results),
        Colors.GREEN if saved_count == 3 else Colors.YELLOW
    )
    
    return saved_count

def agent2_retrieve_url():
    """Agent 2: URL Retriever - Searches and retrieves a specific doc URL"""
    display_agent_card(
        2,
        "🔍 URL Retriever",
        "Information Detective",
        "Search shared memory and extract specific documentation URLs"
    )
    
    query = "stripe checkout"
    show_live_input("Search Query", query, Colors.CYAN)
    
    type_effect("→ Accessing Kinic shared memory...", 0.02)
    type_effect("→ Searching through saved documentation...", 0.02)
    
    start_time = time.time()
    response = requests.post(
        f"{KINIC_API}/search-and-retrieve",
        json={"query": query},
        timeout=60
    )
    elapsed = time.time() - start_time
    
    if response.json().get('success'):
        url = response.json().get('url', '')
        show_live_output("Retrieved URL", url[:60] + "..." if len(url) > 60 else url, True)
        show_live_output("Time", f"{elapsed:.1f} seconds", True)
        
        # Agent summary
        print_box(
            "AGENT 2 RESULTS",
            f"Query: '{query}'\nStatus: ✅ URL Found\nURL: {url[:50]}...\nRetrieval Time: {elapsed:.1f}s",
            Colors.GREEN
        )
        return url
    else:
        show_live_output("Search", "Failed - No URL found", False)
        print_box(
            "AGENT 2 RESULTS",
            f"Query: '{query}'\nStatus: ❌ Failed",
            Colors.RED
        )
        return None

def agent3_extract_insights():
    """Agent 3: AI Analyst - Extracts insights from saved documentation"""
    display_agent_card(
        3,
        "🧠 AI Analyst",
        "Implementation Strategist",
        "Extract actionable insights from collective knowledge"
    )
    
    query = "explain how to implement Stripe payments with best practices"
    show_live_input("AI Query", query, Colors.CYAN)
    
    type_effect("→ Connecting to Kinic AI engine...", 0.02)
    type_effect("→ Analyzing saved Stripe documentation...", 0.02)
    type_effect("→ Generating implementation insights...", 0.02)
    
    print(f"\n{Colors.YELLOW}⏳ AI is thinking (this takes 30-45 seconds)...{Colors.END}")
    
    start_time = time.time()
    response = requests.post(
        f"{KINIC_API}/search-ai-extract",
        json={"query": query},
        timeout=120
    )
    elapsed = time.time() - start_time
    
    if response.json().get('success'):
        ai_response = response.json().get('ai_response', '')
        if ai_response:
            show_live_output("AI Response", f"{len(ai_response)} characters generated", True)
            show_live_output("Generation Time", f"{elapsed:.1f} seconds", True)
            
            # Display AI insights beautifully
            print(f"\n{Colors.BOLD}{Colors.CYAN}🤖 AI INSIGHTS:{Colors.END}")
            print(f"{Colors.GREEN}{'─' * 70}{Colors.END}")
            
            # Wrap text nicely
            words = ai_response.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 > 70:
                    print(f"  {line}")
                    line = word
                else:
                    line = f"{line} {word}" if line else word
            if line:
                print(f"  {line}")
            
            print(f"{Colors.GREEN}{'─' * 70}{Colors.END}")
            
            # Agent summary
            print_box(
                "AGENT 3 RESULTS",
                f"Query: Implementation best practices\nStatus: ✅ Success\nInsights: {len(ai_response)} chars\nTime: {elapsed:.1f}s",
                Colors.GREEN
            )
            return ai_response
    
    show_live_output("AI Analysis", "Failed", False)
    print_box(
        "AGENT 3 RESULTS",
        f"Query: Implementation best practices\nStatus: ❌ Failed",
        Colors.RED
    )
    return None

def show_final_summary(saved_docs, retrieved_url, ai_insights):
    """Display beautiful final summary"""
    print()
    print_colored("═" * 75, Colors.BOLD + Colors.HEADER)
    print_colored("                    🏁 DEMONSTRATION COMPLETE 🏁", Colors.BOLD + Colors.HEADER)
    print_colored("═" * 75, Colors.BOLD + Colors.HEADER)
    
    success_count = sum([
        saved_docs > 0,
        retrieved_url is not None,
        ai_insights is not None
    ])
    
    # Results table
    print(f"\n{Colors.BOLD}📊 FINAL RESULTS ({success_count}/3 Successful):{Colors.END}\n")
    
    print(f"   {Colors.CYAN}Agent 1 - Documentation Collector:{Colors.END}")
    if saved_docs > 0:
        print(f"      {Colors.GREEN}✅ Successfully saved {saved_docs} Stripe docs to blockchain{Colors.END}")
    else:
        print(f"      {Colors.RED}❌ Failed to save documentation{Colors.END}")
    
    print(f"\n   {Colors.CYAN}Agent 2 - URL Retriever:{Colors.END}")
    if retrieved_url:
        print(f"      {Colors.GREEN}✅ Retrieved URL from shared memory{Colors.END}")
        print(f"      {Colors.GREEN}   {retrieved_url[:60]}...{Colors.END}")
    else:
        print(f"      {Colors.RED}❌ Failed to retrieve URL{Colors.END}")
    
    print(f"\n   {Colors.CYAN}Agent 3 - AI Analyst:{Colors.END}")
    if ai_insights:
        print(f"      {Colors.GREEN}✅ Generated {len(ai_insights)} chars of insights{Colors.END}")
    else:
        print(f"      {Colors.RED}❌ Failed to generate insights{Colors.END}")
    
    # Key learnings
    print_box(
        "💡 KEY DEMONSTRATION POINTS",
        """• All 3 agents shared the same Kinic memory
• No direct communication between agents
• Knowledge persisted on blockchain
• Each agent has specialized capabilities
• Collaboration without coordination""",
        Colors.YELLOW
    )
    
    # Call to action
    if success_count == 3:
        print_colored("\n    🎉 PERFECT DEMONSTRATION! All agents succeeded! 🎉", 
                     Colors.BOLD + Colors.GREEN)
        print_colored("\n    Ready to give YOUR AI perfect memory?", Colors.BOLD)
        print_colored("    👉 Get Kinic at: https://kinic.io", Colors.CYAN)
    
    print()

def main():
    """Run the complete visual demonstration"""
    print_header()
    
    # Introduction
    time.sleep(2)
    type_effect("\n📖 THE SCENARIO:", 0.05, Colors.BOLD + Colors.YELLOW)
    type_effect("A development team needs to integrate Stripe payments.", 0.03)
    type_effect("Three specialized AI agents will collaborate through Kinic's", 0.03)
    type_effect("blockchain memory to research, analyze, and provide insights.", 0.03)
    
    time.sleep(2)
    
    # Check API
    print(f"\n{Colors.YELLOW}🔍 Checking systems...{Colors.END}")
    try:
        response = requests.get(KINIC_API, timeout=5)
        if response.status_code == 200:
            config = response.json().get('config', {})
            show_live_output("Kinic API", "Online ✅", True)
            show_live_output("Kinic Button", f"({config.get('kinic_x')}, {config.get('kinic_y')})", True)
            show_live_output("AI Response", f"({config.get('ai_response_x')}, {config.get('ai_response_y')})", True)
        else:
            show_live_output("API Status", "Error", False)
            return
    except Exception as e:
        show_live_output("Connection", f"Failed: {e}", False)
        print_colored("\n⚠️  Please start the API: python kinic-api.py", Colors.RED)
        return
    
    print(f"\n{Colors.BOLD}⚠️  Ensure Chrome is open with Kinic extension visible{Colors.END}")
    input(f"\n{Colors.GREEN}Press Enter to begin the demonstration...{Colors.END}")
    
    # Dramatic start
    print()
    countdown(3, "Initiating multi-agent collaboration in")
    
    # Run agents with proper spacing
    print_colored("\n" + "─" * 75, Colors.BLUE)
    print_colored("PHASE 1: KNOWLEDGE COLLECTION", Colors.BOLD + Colors.BLUE)
    print_colored("─" * 75, Colors.BLUE)
    saved_docs = agent1_save_stripe_docs()
    
    if saved_docs == 0:
        print_colored("\n⚠️ No documents saved. Check Chrome and Kinic setup.", Colors.RED)
        return
    
    countdown(5, "Phase 2 starting in")
    
    print_colored("\n" + "─" * 75, Colors.BLUE)
    print_colored("PHASE 2: INFORMATION RETRIEVAL", Colors.BOLD + Colors.BLUE)
    print_colored("─" * 75, Colors.BLUE)
    retrieved_url = agent2_retrieve_url()
    
    countdown(5, "Phase 3 starting in")
    
    print_colored("\n" + "─" * 75, Colors.BLUE)
    print_colored("PHASE 3: AI ANALYSIS", Colors.BOLD + Colors.BLUE)
    print_colored("─" * 75, Colors.BLUE)
    ai_insights = agent3_extract_insights()
    
    # Final summary
    show_final_summary(saved_docs, retrieved_url, ai_insights)
    
    # Save results with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"stripe_demo_visual_{timestamp}.txt"
    
    with open(results_file, "w") as f:
        f.write("Stripe Multi-Agent Demo - Visual Version\n")
        f.write(f"Timestamp: {datetime.now()}\n\n")
        f.write(f"Results:\n")
        f.write(f"  Agent 1: Saved {saved_docs} documents\n")
        f.write(f"  Agent 2: Retrieved URL: {retrieved_url or 'None'}\n")
        f.write(f"  Agent 3: AI Insights: {len(ai_insights) if ai_insights else 0} characters\n")
        if ai_insights:
            f.write(f"\nAI Response:\n{ai_insights}\n")
    
    print_colored(f"\n📄 Detailed results saved to: {results_file}", Colors.CYAN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️ Demo interrupted by user", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n\n❌ Error: {e}", Colors.RED)
        print_colored("Please check that the Kinic API is running correctly", Colors.RED)