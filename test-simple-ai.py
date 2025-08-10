#!/usr/bin/env python3
"""Simple test of AI extraction"""

import requests
import json

print("Testing AI extraction with simple query...")
print("This will search for 'JavaScript' and extract AI response\n")

response = requests.post("http://localhost:5006/search-ai-extract",
                         json={"query": "JavaScript"})

if response.status_code == 200:
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Query: {data.get('query')}")
    print(f"\nAI Response ({len(data.get('ai_response', ''))} chars):")
    print("-" * 50)
    print(data.get('ai_response', 'No response'))
    print("-" * 50)
else:
    print(f"Error: {response.status_code}")
    print(response.text)