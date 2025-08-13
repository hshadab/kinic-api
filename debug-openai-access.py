#!/usr/bin/env python3
"""Debug OpenAI API access issues"""

import os
from openai import OpenAI

def debug_openai_access():
    """Debug what's happening with OpenAI API access"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return
    
    print(f"🔑 Testing API key: {api_key[:12]}...{api_key[-8:]}")
    
    client = OpenAI(api_key=api_key)
    
    # Test 1: List all available models
    print("\n📋 STEP 1: Listing available models...")
    try:
        models = client.models.list()
        model_ids = [model.id for model in models.data]
        
        print(f"✅ Total models available: {len(model_ids)}")
        
        # Check for GPT-5 family
        gpt5_models = [m for m in model_ids if "gpt-5" in m]
        gpt4_models = [m for m in model_ids if "gpt-4" in m]
        
        print(f"\n🎯 GPT-5 models found: {len(gpt5_models)}")
        for model in gpt5_models:
            print(f"   ✅ {model}")
        
        print(f"\n🤖 GPT-4 models found: {len(gpt4_models)}")
        for model in gpt4_models[:3]:  # Show first 3
            print(f"   ✅ {model}")
            
    except Exception as e:
        print(f"❌ Models list failed: {e}")
        return
    
    # Test 2: Try GPT-5-mini specifically
    print(f"\n🧪 STEP 2: Testing GPT-5-mini direct call...")
    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": "Reply with exactly: TEST SUCCESS"}],
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        print(f"✅ GPT-5-mini works! Response: '{result}'")
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ GPT-5-mini failed: {error_str}")
        
        # Analyze the error
        if "does not exist" in error_str:
            print("🔍 ERROR TYPE: Model doesn't exist for this key")
        elif "access" in error_str.lower():
            print("🔍 ERROR TYPE: Access denied")
        elif "quota" in error_str.lower():
            print("🔍 ERROR TYPE: Quota/billing issue")
        elif "rate_limit" in error_str.lower():
            print("🔍 ERROR TYPE: Rate limit")
        else:
            print(f"🔍 ERROR TYPE: Unknown - {error_str[:100]}")
    
    # Test 3: Try GPT-4o-mini as baseline
    print(f"\n🧪 STEP 3: Testing GPT-4o-mini as baseline...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply with exactly: BASELINE SUCCESS"}],
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        print(f"✅ GPT-4o-mini works! Response: '{result}'")
        
    except Exception as e:
        print(f"❌ GPT-4o-mini also failed: {e}")
        print("🚨 This suggests a broader API key issue")
    
    # Test 4: Account/usage info
    print(f"\n📊 STEP 4: Checking account info...")
    try:
        # Try to get account info (this might not work with newer API versions)
        print("ℹ️  Account details not accessible via API")
        
    except Exception as e:
        print(f"ℹ️  Account info check failed (expected): {e}")

if __name__ == "__main__":
    print("🔬 DEBUGGING OPENAI API ACCESS")
    print("=" * 50)
    debug_openai_access()
    
    print(f"\n💡 POSSIBLE SOLUTIONS:")
    print(f"1. Wait 5-10 minutes - new keys sometimes need propagation time")
    print(f"2. Check if key was created from the SAME account showing GPT-5 limits") 
    print(f"3. Verify key has correct permissions/scope")
    print(f"4. Try regenerating the key")
    print(f"5. Contact OpenAI support if dashboard shows access but API denies it")