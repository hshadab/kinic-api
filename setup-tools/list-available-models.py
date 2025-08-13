#!/usr/bin/env python3
"""List all models available to your OpenAI account"""

import os
from openai import OpenAI

def list_models():
    """List all available models for this API key"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return
    
    print(f"🔑 Using API key: {api_key[:12]}...")
    
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        
        print(f"\n📋 Available Models ({len(models.data)} total):")
        print("=" * 50)
        
        # Sort models by name
        sorted_models = sorted(models.data, key=lambda x: x.id)
        
        gpt5_models = []
        gpt4_models = []
        other_models = []
        
        for model in sorted_models:
            if "gpt-5" in model.id:
                gpt5_models.append(model.id)
            elif "gpt-4" in model.id:
                gpt4_models.append(model.id)
            else:
                other_models.append(model.id)
        
        if gpt5_models:
            print("\n🎯 GPT-5 MODELS AVAILABLE:")
            for model in gpt5_models:
                print(f"  ✅ {model}")
        else:
            print("\n❌ No GPT-5 models found")
        
        if gpt4_models:
            print("\n🤖 GPT-4 MODELS AVAILABLE:")
            for model in gpt4_models[:5]:  # Show first 5
                print(f"  ✅ {model}")
            if len(gpt4_models) > 5:
                print(f"  ... and {len(gpt4_models) - 5} more GPT-4 models")
        
        print(f"\n📊 SUMMARY:")
        print(f"  • GPT-5 models: {len(gpt5_models)}")
        print(f"  • GPT-4 models: {len(gpt4_models)}")
        print(f"  • Other models: {len(other_models)}")
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    print("📋 LISTING AVAILABLE OPENAI MODELS")
    print("=" * 40)
    list_models()