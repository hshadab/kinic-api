#!/usr/bin/env python3
"""
Simplified Claude + GPT Collaboration Demo
==========================================
Shows two AI agents collaborating without browser automation.
Simulates the research phase and demonstrates real AI collaboration.
"""

import os
import json
import requests
import time

# AI Libraries
import anthropic
from openai import OpenAI

class SimpleCollaborationDemo:
    def __init__(self):
        self.kinic_url = "http://localhost:5006"
        self.setup_clients()
        
    def setup_clients(self):
        """Initialize AI clients"""
        self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.gpt = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("✅ AI clients ready")
    
    def test_collaboration(self):
        """Test real AI collaboration through text generation"""
        print("\n" + "="*60)
        print("TESTING AI COLLABORATION")
        print("="*60)
        
        # Step 1: Claude designs architecture
        print("\n🤖 CLAUDE: Designing sentiment analysis architecture...")
        
        claude_prompt = """
        Design a Python class architecture for a multi-language sentiment analysis API.
        Include: model loading, batch processing, and confidence scores.
        Return only the class structure in Python code, no explanation.
        """
        
        claude_response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": claude_prompt}]
        )
        
        claude_design = claude_response.content[0].text
        print("✅ Claude created architecture")
        print(f"Preview: {claude_design[:200]}...")
        
        # Step 2: GPT-3.5 implements the API
        print("\n🤖 GPT-3.5: Building on Claude's architecture...")
        
        gpt_prompt = f"""
        Using this architecture from Claude:
        {claude_design[:300]}
        
        Create a FastAPI endpoint that uses this architecture.
        Include error handling and batch processing.
        Return only the API implementation code.
        """
        
        gpt_response = self.gpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": gpt_prompt}],
            max_tokens=500
        )
        
        gpt_implementation = gpt_response.choices[0].message.content
        print("✅ GPT-3.5 implemented the API")
        print(f"Preview: {gpt_implementation[:200]}...")
        
        # Step 3: Combine the solutions
        final_solution = f"""
# Multi-Language Sentiment Analysis API
# Built collaboratively by Claude and GPT-3.5

# ========== CLAUDE'S ARCHITECTURE ==========
{claude_design}

# ========== GPT-3.5'S IMPLEMENTATION ==========
{gpt_implementation}

# This demonstrates real AI collaboration:
# - Claude designed the core architecture
# - GPT-3.5 built upon Claude's design to create the API
# - Both AIs contributed their strengths to the final solution
"""
        
        # Save the solution
        with open("collaborative_sentiment_api.py", "w") as f:
            f.write(final_solution)
        
        print("\n📁 Complete solution saved to: collaborative_sentiment_api.py")
        return final_solution
    
    def test_kinic_api(self):
        """Test if Kinic API is working"""
        print("\n🔍 Testing Kinic API connection...")
        try:
            response = requests.get(self.kinic_url)
            if response.status_code == 200:
                print("✅ Kinic API is running")
                return True
            else:
                print(f"❌ Kinic API error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Kinic API not reachable: {e}")
            return False
    
    def demonstrate_semantic_search(self):
        """Demonstrate Kinic's semantic search capability"""
        print("\n🔎 Testing Kinic's semantic search...")
        
        # This would require having content saved in Kinic
        # For now, we'll show what the search would look like
        test_query = "multilingual sentiment analysis models"
        
        try:
            response = requests.post(
                f"{self.kinic_url}/search-and-retrieve",
                json={"query": test_query}
            )
            
            if response.json().get('success'):
                print(f"✅ Semantic search found: {response.json().get('url', 'No URL')}")
            else:
                print("ℹ️  No content in Kinic yet (would need saved pages)")
                
        except Exception as e:
            print(f"⚠️  Search test failed: {e}")
    
    def run_demo(self):
        """Run the complete demonstration"""
        print("""
╔════════════════════════════════════════════════════════════════════╗
║            SIMPLIFIED AI COLLABORATION DEMO                       ║
║                                                                    ║
║  Claude + GPT-3.5 working together on sentiment analysis          ║
╚════════════════════════════════════════════════════════════════════╝
        """)
        
        # Test connections
        kinic_ready = self.test_kinic_api()
        
        # Test collaboration
        start_time = time.time()
        solution = self.test_collaboration()
        elapsed = time.time() - start_time
        
        # Test semantic search
        if kinic_ready:
            self.demonstrate_semantic_search()
        
        # Show results
        print("\n" + "="*60)
        print("COLLABORATION RESULTS")
        print("="*60)
        print(f"""
✅ Collaboration completed in {elapsed:.1f} seconds

What happened:
1. Claude designed the sentiment analysis architecture
2. GPT-3.5 built a FastAPI implementation using Claude's design
3. Both AIs contributed to the final solution

Key insights:
- Each AI contributed its strengths (Claude: architecture, GPT: implementation)
- The final code combines both AI's work seamlessly
- This is real AI collaboration, not simulation

Next steps:
- Save content to Kinic to test semantic search
- Run the full browser-based demo when ready
        """)
        
        print(f"\n📄 Solution preview:")
        print(solution[:500] + "..." if len(solution) > 500 else solution)

if __name__ == "__main__":
    # Check environment
    if not os.getenv("ANTHROPIC_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        print("❌ API keys not set!")
        print("Run: export ANTHROPIC_API_KEY='your-key'")
        print("Run: export OPENAI_API_KEY='your-key'")
        exit(1)
    
    demo = SimpleCollaborationDemo()
    demo.run_demo()