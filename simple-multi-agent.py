#!/usr/bin/env python3
"""
Simple Multi-Agent Demo - Code Review Pipeline
Two agents collaborating: one saves code, another reviews it
"""

import requests
import time

KINIC_API = "http://localhost:5005"

def agent1_save_code():
    """Agent 1: Saves code examples to Kinic"""
    print("\n🤖 AGENT 1 (Code Collector)")
    print("→ Saving Python code examples to shared memory...")
    
    # Navigate to a Python tutorial or GitHub repo
    input("\nPlease navigate to a Python code page in Chrome, then press Enter...")
    
    response = requests.post(f"{KINIC_API}/save")
    print("✓ Code saved to Kinic memory")
    return response.json()

def agent2_review_code():
    """Agent 2: Reviews saved code"""
    print("\n🤖 AGENT 2 (Code Reviewer)")
    print("→ Searching shared memory for Python code...")
    
    time.sleep(2)
    
    # Search for Python code
    review = requests.post(
        f"{KINIC_API}/search-ai-extract",
        json={"query": "review the Python code for best practices"}
    )
    
    if review.json().get('success'):
        print("\n📝 Code Review Results:")
        print(review.json().get('ai_response', 'No review available'))
    
    return review.json()

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║   SIMPLE MULTI-AGENT DEMO WITH KINIC  ║
    ╚════════════════════════════════════════╝
    
    Watch two agents share knowledge:
    • Agent 1 saves code to Kinic
    • Agent 2 reviews it from shared memory
    """)
    
    # Agent 1 does its work
    agent1_save_code()
    
    print("\n" + "="*40)
    print("Switching to Agent 2...")
    print("="*40)
    
    # Agent 2 accesses the same memory
    agent2_review_code()
    
    print("\n✅ Demo complete! Both agents used the same Kinic memory.")

if __name__ == "__main__":
    main()