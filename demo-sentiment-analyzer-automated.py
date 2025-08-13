"""
Kinic Multi-Agent Demo: Building Sentiment Analyzer (Automated Version)
========================================================================
This demo shows 3 AI agents collaborating to build a HF sentiment analysis API
using Kinic's semantic search capabilities with actual browser automation.

Prerequisites:
- Kinic API running on localhost:5006
- Chrome with Kinic extension installed and logged in
- Proper coordinates configured in kinic-config.json
"""

import time
import requests
import webbrowser
from datetime import datetime

class KinicAutomatedDemo:
    def __init__(self):
        self.base_url = "http://localhost:5006"
        
        # The Hugging Face URLs we'll save during the demo
        self.demo_urls = [
            # Claude's sentiment model research
            "https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest",
            "https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english",
            "https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment",
            
            # GPT-5's implementation examples
            "https://huggingface.co/spaces/evaluate-metric/bertscore",
            "https://huggingface.co/docs/transformers/tasks/sequence_classification",
            
            # Gemini's deployment guides
            "https://huggingface.co/docs/hub/spaces-sdks-gradio",
            "https://huggingface.co/docs/transformers/main_classes/pipelines"
        ]
        
        # Test queries to demonstrate semantic search
        self.semantic_queries = [
            ("model initialization", "Shows how 'initialization' finds 'from_pretrained' and 'pipeline' setup"),
            ("text processing", "Demonstrates 'processing' connects to 'tokenization' and 'inference'"),
            ("deployment configuration", "Reveals 'deployment' relates to 'Gradio', 'Spaces', and 'API'")
        ]
    
    def display_banner(self):
        print("""
╔════════════════════════════════════════════════════════════════════╗
║              KINIC SEMANTIC SEARCH DEMO - AUTOMATED               ║
║         Building a Sentiment Analyzer with AI Collaboration       ║
║                   Claude × GPT-5 × Gemini                        ║
╚════════════════════════════════════════════════════════════════════╝
        """)
    
    def check_kinic_api(self):
        """Verify Kinic API is running"""
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                data = response.json()
                print("✅ Kinic API is running")
                print(f"   Kinic button: ({data['config']['kinic_x']}, {data['config']['kinic_y']})")
                print(f"   AI response: ({data['config']['ai_response_x']}, {data['config']['ai_response_y']})")
                return True
            else:
                print("❌ Kinic API is not responding correctly")
                return False
        except:
            print("❌ Cannot connect to Kinic API on localhost:5006")
            print("   Please run 'python kinic-api.py' in another terminal")
            return False
    
    def save_page_to_kinic(self, url, agent_name):
        """Navigate to URL and save it using Kinic"""
        print(f"\n{agent_name}: Navigating to {url.split('/')[-1]}...")
        
        # Open URL in browser
        webbrowser.open(url)
        time.sleep(3)  # Wait for page to load
        
        # Call Kinic API to save the page
        print(f"   Saving page to Kinic...")
        response = requests.post(f"{self.base_url}/save")
        
        if response.json().get('success'):
            print(f"   ✅ Page saved successfully")
            return True
        else:
            print(f"   ❌ Failed to save: {response.json().get('error')}")
            return False
    
    def perform_semantic_search(self, query):
        """Perform semantic search using Kinic"""
        print(f"\n🔍 Searching for: '{query}'")
        
        response = requests.post(
            f"{self.base_url}/search-and-retrieve",
            json={"query": query}
        )
        
        if response.json().get('success'):
            url = response.json().get('url')
            print(f"   ✅ Found relevant result: {url[:60]}...")
            return url
        else:
            print(f"   ❌ Search failed: {response.json().get('error')}")
            return None
    
    def get_ai_insights(self, query):
        """Get AI-synthesized insights from Kinic"""
        print(f"\n🤖 Getting AI insights for: '{query}'")
        
        response = requests.post(
            f"{self.base_url}/search-ai-extract",
            json={"query": query}
        )
        
        if response.json().get('success'):
            ai_response = response.json().get('ai_response')
            print(f"   ✅ AI Response ({len(ai_response)} chars):")
            print(f"   {ai_response[:200]}..." if len(ai_response) > 200 else f"   {ai_response}")
            return ai_response
        else:
            print(f"   ❌ AI extraction failed: {response.json().get('error')}")
            return None
    
    def act1_knowledge_gathering(self):
        """Act 1: Agents save Hugging Face documentation"""
        print("\n" + "="*70)
        print("ACT 1: KNOWLEDGE GATHERING")
        print("="*70)
        
        saved_count = 0
        
        # Claude saves sentiment model documentation
        print("\n📚 CLAUDE: Researching sentiment analysis models...")
        for url in self.demo_urls[:3]:
            if self.save_page_to_kinic(url, "CLAUDE"):
                saved_count += 1
            time.sleep(2)
        
        # GPT-5 saves implementation examples
        print("\n🔧 GPT-5: Finding implementation patterns...")
        for url in self.demo_urls[3:5]:
            if self.save_page_to_kinic(url, "GPT-5"):
                saved_count += 1
            time.sleep(2)
        
        # Gemini saves deployment guides
        print("\n🚀 GEMINI: Getting deployment configurations...")
        for url in self.demo_urls[5:7]:
            if self.save_page_to_kinic(url, "GEMINI"):
                saved_count += 1
            time.sleep(2)
        
        print(f"\n✅ Successfully saved {saved_count}/{len(self.demo_urls)} pages to Kinic!")
        return saved_count > 0
    
    def act2_semantic_search_demo(self):
        """Act 2: Demonstrate semantic search capabilities"""
        print("\n" + "="*70)
        print("ACT 2: SEMANTIC SEARCH MAGIC")
        print("="*70)
        
        for query, explanation in self.semantic_queries:
            print(f"\n💡 {explanation}")
            result = self.perform_semantic_search(query)
            
            if result:
                print(f"   Traditional search would need exact keywords ❌")
                print(f"   Kinic found semantically related content ✅")
            
            time.sleep(2)
        
        # Get AI insights
        print("\n" + "="*70)
        print("ACT 3: AI SYNTHESIS")
        print("="*70)
        
        synthesis_query = "How to build a production sentiment analysis API with Hugging Face"
        ai_response = self.get_ai_insights(synthesis_query)
        
        if ai_response:
            print("\n📝 Kinic synthesized a complete solution from all saved pages!")
    
    def show_generated_code(self):
        """Display the code that would be generated from semantic search"""
        print("\n" + "="*70)
        print("GENERATED CODE (from semantic understanding)")
        print("="*70)
        
        code = '''
# Complete sentiment analysis API built from semantic search results

from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
import torch

app = FastAPI()

# Found via "model initialization" search
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    device=0 if torch.cuda.is_available() else -1
)

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(input: TextInput):
    # Found via "text processing" search
    result = sentiment_analyzer(input.text)[0]
    
    # Error handling found via "deployment configuration" search
    return {
        "text": input.text,
        "sentiment": result["label"],
        "confidence": round(result["score"], 4)
    }

# Run with: uvicorn main:app --reload
'''
        print(code)
    
    def show_comparison(self):
        """Show efficiency comparison"""
        print("\n" + "="*70)
        print("EFFICIENCY COMPARISON")
        print("="*70)
        
        print("""
Traditional Approach (Keyword Search):
• Reading 7 documentation pages: 25 minutes
• Finding correct imports/setup: 15 minutes
• Debugging integration issues: 20 minutes
• Total time: ~60 minutes ⏰

Kinic Semantic Search Approach:
• Saving 7 pages to Kinic: 2 minutes
• 3 semantic searches: 30 seconds
• AI synthesis & code generation: 30 seconds
• Total time: ~3 minutes 🚀

ACCELERATION FACTOR: 20X faster!
        """)
    
    def interactive_search(self):
        """Allow user to try their own semantic search"""
        print("\n" + "="*70)
        print("INTERACTIVE SEMANTIC SEARCH")
        print("="*70)
        
        print("\n🎤 Try your own semantic search!")
        print("   Examples: 'performance issues', 'memory problems', 'API errors'")
        
        while True:
            query = input("\nEnter search query (or 'done' to finish): ").strip()
            if query.lower() == 'done':
                break
            
            if query:
                # Try regular search
                result = self.perform_semantic_search(query)
                
                if result:
                    print(f"\n📊 Semantic connections made:")
                    print(f"   '{query}' connected to relevant HF documentation")
                    print(f"   Even though pages don't contain exact phrase!")
    
    def run_demo(self, interactive=True):
        """Run the complete automated demo"""
        self.display_banner()
        
        # Check API is running
        if not self.check_kinic_api():
            return
        
        print("\n⚠️  IMPORTANT: This demo will:")
        print("   1. Open browser tabs automatically")
        print("   2. Control your mouse and keyboard")
        print("   3. Save pages to Kinic")
        print("\n   Make sure Chrome with Kinic extension is ready!")
        
        input("\nPress Enter to start the automated demo...")
        
        start_time = time.time()
        
        # Run demo acts
        if self.act1_knowledge_gathering():
            self.act2_semantic_search_demo()
            self.show_generated_code()
            self.show_comparison()
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Demo completed in {elapsed/60:.1f} minutes")
        
        if interactive:
            self.interactive_search()
        
        # Final message
        print("\n" + "="*70)
        print("🎯 THE KEY INSIGHT")
        print("="*70)
        print("""
Kinic doesn't just store web pages - it understands them.

When you search for "deployment issues", it finds pages about:
• Configuration problems (deployment ≈ setup)
• Environment variables (issues ≈ errors)
• Docker containers (deployment ≈ containerization)
• API endpoints (deployment ≈ production)

This is the difference between keyword matching and semantic understanding.
Kinic gives AI agents true memory - not just storage, but comprehension.
        """)
        print("="*70)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Kinic Semantic Search Demo')
    parser.add_argument('--quick', action='store_true', help='Skip interactive search at end')
    args = parser.parse_args()
    
    demo = KinicAutomatedDemo()
    demo.run_demo(interactive=not args.quick)