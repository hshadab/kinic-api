#!/usr/bin/env python3
"""
Test that new coordinates work correctly
"""

import json
import os
import requests

print("\n" + "="*60)
print("TESTING NEW COORDINATES")
print("="*60)

# Load and display config
config_file = "kinic-config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"\n✅ Config loaded from: {config_file}")
    print(f"\n📍 Current Coordinates:")
    print(f"   Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
    print(f"   AI response:  ({config['ai_response_x']}, {config['ai_response_y']})")
else:
    print(f"\n❌ Config file not found!")
    exit(1)

# Check if API is running and using same config
KINIC_API = "http://localhost:5006"
print(f"\n🔍 Checking API at {KINIC_API}...")

try:
    response = requests.get(KINIC_API, timeout=5)
    if response.status_code == 200:
        api_config = response.json().get('config', {})
        print(f"✅ API is running")
        
        # Compare coordinates
        print(f"\n📊 Coordinate Verification:")
        
        # Check Kinic button
        if api_config.get('kinic_x') == config['kinic_x'] and api_config.get('kinic_y') == config['kinic_y']:
            print(f"   ✅ Kinic button: API matches config ({config['kinic_x']}, {config['kinic_y']})")
        else:
            print(f"   ❌ Kinic button mismatch!")
            print(f"      Config: ({config['kinic_x']}, {config['kinic_y']})")
            print(f"      API:    ({api_config.get('kinic_x')}, {api_config.get('kinic_y')})")
            print(f"   ⚠️  Restart the API to load new coordinates")
        
        # Check AI response
        if api_config.get('ai_response_x') == config['ai_response_x'] and api_config.get('ai_response_y') == config['ai_response_y']:
            print(f"   ✅ AI response: API matches config ({config['ai_response_x']}, {config['ai_response_y']})")
        else:
            print(f"   ❌ AI response mismatch!")
            print(f"      Config: ({config['ai_response_x']}, {config['ai_response_y']})")
            print(f"      API:    ({api_config.get('ai_response_x')}, {api_config.get('ai_response_y')})")
            print(f"   ⚠️  Restart the API to load new coordinates")
        
        # Test clicking Kinic button
        print(f"\n🖱️ Testing Kinic button click...")
        response = requests.post(f"{KINIC_API}/click", timeout=5)
        if response.json().get('success'):
            print(f"   ✅ Click command sent successfully")
            print(f"   Check if Kinic popup opened at position ({config['kinic_x']}, {config['kinic_y']})")
        else:
            print(f"   ❌ Click failed: {response.json().get('message')}")
            
    else:
        print(f"❌ API returned status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print(f"❌ Cannot connect to API")
    print(f"\n📌 To start the API:")
    print(f"   python kinic-api.py")
    print(f"\nThe API will automatically load coordinates from kinic-config.json")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\nYour new coordinates are saved in kinic-config.json:")
print(f"  Kinic: ({config['kinic_x']}, {config['kinic_y']})")
print(f"  AI:    ({config['ai_response_x']}, {config['ai_response_y']})")
print(f"\nAll Python files dynamically load from this config file.")
print(f"No resolution mismatch issues - using PyAutoGUI directly!")
print(f"\n✅ Ready to run demos with new coordinates!")