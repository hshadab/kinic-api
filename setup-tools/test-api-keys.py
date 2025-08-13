#!/usr/bin/env python3
"""Test API keys for Claude and OpenAI"""

import os
import sys

def test_claude():
    """Test Anthropic Claude API"""
    try:
        import anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found")
            return False
        
        print(f"🔑 Claude API Key: {api_key[:12]}...")
        
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'Claude API working!' in exactly those words."}]
        )
        
        result = response.content[0].text.strip()
        print(f"🤖 Claude response: {result}")
        
        if "Claude API working!" in result:
            print("✅ Claude API: WORKING")
            return True
        else:
            print("⚠️ Claude API: Unexpected response")
            return False
            
    except ImportError:
        print("❌ anthropic library not installed: pip install anthropic")
        return False
    except Exception as e:
        print(f"❌ Claude API error: {e}")
        return False

def test_openai():
    """Test OpenAI GPT API"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found")
            return False
        
        print(f"🔑 OpenAI API Key: {api_key[:12]}...")
        
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": "Say 'GPT-5-mini API working!' in exactly those words."}],
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip()
        print(f"🤖 GPT-5-mini response: {result}")
        
        if "GPT-5-mini API working!" in result:
            print("✅ GPT-5-mini API: WORKING")
            return True
        else:
            print("⚠️ GPT-5-mini API: Unexpected response")
            return False
            
    except ImportError:
        print("❌ openai library not installed: pip install openai")
        return False
    except Exception as e:
        print(f"❌ GPT-5-mini API error: {e}")
        # Try fallback to gpt-4o-mini
        try:
            print("🔄 Trying fallback to gpt-4o-mini...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say 'GPT-4o-mini API working!' in exactly those words."}],
                max_tokens=50
            )
            result = response.choices[0].message.content.strip()
            print(f"🤖 GPT-4o-mini response: {result}")
            print("✅ GPT-4o-mini API: WORKING (fallback)")
            return True
        except Exception as e2:
            print(f"❌ Both GPT-5-mini and GPT-4o-mini failed: {e2}")
            return False

def main():
    print("🧪 TESTING API KEYS")
    print("=" * 50)
    
    claude_ok = test_claude()
    print()
    openai_ok = test_openai()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    print(f"Claude API: {'✅ WORKING' if claude_ok else '❌ FAILED'}")
    print(f"OpenAI API: {'✅ WORKING' if openai_ok else '❌ FAILED'}")
    
    if claude_ok and openai_ok:
        print("\n🎉 Both APIs working! Ready to run demos!")
        return True
    else:
        print("\n⚠️ Fix API issues before running demos")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)