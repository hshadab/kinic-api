#!/usr/bin/env python3
"""Test GPT-5-mini access specifically"""

import os
from openai import OpenAI

def test_gpt5_mini():
    """Test if GPT-5-mini is available"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return False
    
    print(f"🔑 Testing with API key: {api_key[:12]}...")
    
    client = OpenAI(api_key=api_key)
    
    try:
        print("🧪 Testing GPT-5-mini...")
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": "Say 'GPT-5-mini working!' in exactly those words."}],
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ GPT-5-mini response: {result}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ GPT-5-mini failed: {error_msg}")
        
        if "does not exist" in error_msg or "Invalid model" in error_msg:
            print("📋 GPT-5-mini not available on your account")
            print("💡 You may need:")
            print("   1. Account upgrade/waitlist approval")
            print("   2. New API key with GPT-5 access")
            print("   3. Check OpenAI dashboard for model availability")
        elif "insufficient_quota" in error_msg:
            print("💳 Account has insufficient credits")
        elif "rate_limit" in error_msg:
            print("⏱️  Rate limited - try again in a moment")
        
        return False

if __name__ == "__main__":
    print("🔬 GPT-5-MINI ACCESS TEST")
    print("=" * 40)
    success = test_gpt5_mini()
    
    if success:
        print("\n🎉 GPT-5-mini is working!")
    else:
        print("\n⚠️  GPT-5-mini not accessible - stick with gpt-4o-mini for now")