#!/usr/bin/env python3
"""
Kinic API - The simplest way to use Kinic in your workflows

Just run: python kinic-api.py
Then use the API endpoints in n8n, Make, Zapier, or any tool!
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime

# Check dependencies
try:
    import pyautogui
    import pyperclip
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError:
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "flask", "flask-cors", "pyperclip"])
    print("✅ Packages installed! Please run the script again.")
    sys.exit(0)

app = Flask(__name__)
CORS(app)

# Simple config file
CONFIG_FILE = 'kinic-config.json'
config = {}

def first_time_setup():
    """Super simple setup - just find the Kinic icon"""
    print("\n🚀 KINIC API - First Time Setup")
    print("="*40)
    print("\n3 quick steps:")
    print("1. Make sure Chrome is open")
    print("2. Make sure you can see the Kinic icon")
    print("3. Click the Kinic icon once to test it\n")
    
    input("Press ENTER when ready...")
    
    print("\n📍 Now hover your mouse over the Kinic icon")
    print("   (Don't click - just hover)")
    print("\n⏰ Recording position in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    x, y = pyautogui.position()
    print(f"\n✅ Got it! Kinic icon is at position ({x}, {y})")
    
    # Save config
    config = {'kinic_x': x, 'kinic_y': y}
    
    # Ask if user wants to set up AI response position
    setup_ai = input("\n🤖 Do you want to set up AI response text position? (y/n): ")
    if setup_ai.lower() == 'y':
        print("\n📝 Let's find where AI responses appear:")
        print("1. I'll open Kinic and run a test query")
        print("2. When you see the AI response, hover your mouse over the text")
        print("3. I'll record that position\n")
        
        input("Press ENTER to start...")
        
        # Run a test query
        pyautogui.click(x, y)  # Click Kinic icon
        time.sleep(2)
        
        print("\n⏰ Please hover over the AI response text area in 5 seconds...")
        for i in range(5, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
        
        resp_x, resp_y = pyautogui.position()
        config['ai_response_x'] = resp_x
        config['ai_response_y'] = resp_y
        print(f"\n✅ AI response position recorded: ({resp_x}, {resp_y})")
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    
    print("\n✨ Setup complete! Your API is ready to use.")
    return config

# Load or create config
try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
except:
    config = first_time_setup()

# Core functions
def click_kinic():
    """Click the Kinic extension icon"""
    pyautogui.click(config['kinic_x'], config['kinic_y'])
    time.sleep(2)

def save_current_page():
    """Save the current page to Kinic"""
    click_kinic()
    time.sleep(4)  # Wait for page context
    pyautogui.hotkey('shift', 'tab')
    time.sleep(0.5)
    pyautogui.press('enter')

def search_kinic(query):
    """Search in Kinic"""
    click_kinic()
    for _ in range(4):
        pyautogui.press('tab')
        time.sleep(0.2)
    pyautogui.typewrite(query)
    pyautogui.press('enter')

def search_and_ai(query, extract_response=True):
    """Search in Kinic and then run AI on the results"""
    # First perform the search
    click_kinic()
    for _ in range(4):
        pyautogui.press('tab')
        time.sleep(0.2)
    pyautogui.typewrite(query)
    pyautogui.press('enter')
    
    # Wait for search results to load
    time.sleep(3)
    
    # Now run AI on the results (Tab 5 times then Enter)
    for _ in range(5):
        pyautogui.press('tab')
        time.sleep(0.2)
    pyautogui.press('enter')
    
    if extract_response:
        # Wait for AI response to generate
        time.sleep(5)  # Adjust based on typical response time
        
        # Get the AI response text position from config or use default
        response_x = config.get('ai_response_x', config['kinic_x'])
        response_y = config.get('ai_response_y', config['kinic_y'] + 200)
        
        # Move to the AI response area and triple-click to select all
        pyautogui.moveTo(response_x, response_y)
        pyautogui.click(clicks=3, interval=0.1)  # Triple click to select paragraph
        
        # Copy to clipboard
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        
        # Get text from clipboard
        time.sleep(0.5)
        ai_response = pyperclip.paste()
        
        return ai_response
    
    return None

# API Routes
@app.route('/')
def home():
    return f'''
    <h1>🎉 Kinic API is Running!</h1>
    <p>Your Kinic is now accessible via API</p>
    
    <h2>Quick Test:</h2>
    <button onclick="fetch('/api/save', {{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{url:window.location.href}})}}).then(r=>r.json()).then(d=>alert('Saved!'))">Save This Page</button>
    <button onclick="testSearchAI()">Search + AI Analysis</button>
    
    <div id="ai-response" style="margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; display: none;">
        <h3>AI Response:</h3>
        <pre id="ai-text" style="white-space: pre-wrap; font-family: Arial, sans-serif;"></pre>
    </div>
    
    <script>
    async function testSearchAI() {{
        const query = prompt('Search query:');
        if (!query) return;
        
        const responseDiv = document.getElementById('ai-response');
        const textDiv = document.getElementById('ai-text');
        
        responseDiv.style.display = 'block';
        textDiv.textContent = 'Loading... Please wait while Kinic processes your query...';
        
        try {{
            const response = await fetch('/api/search-ai', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{query: query}})
            }});
            
            const data = await response.json();
            
            if (data.ai_response) {{
                textDiv.textContent = data.ai_response;
            }} else {{
                textDiv.textContent = 'AI response extraction not available. Response: ' + data.message;
            }}
        }} catch (error) {{
            textDiv.textContent = 'Error: ' + error.message;
        }}
    }}
    </script>
    
    <h2>API Endpoints:</h2>
    <pre>
POST /api/save         - Save a URL to Kinic
POST /api/search       - Search in Kinic
POST /api/search-ai    - Search + AI analysis (NEW!)
POST /api/ai           - Run AI query
    </pre>
    
    <h2>Search + AI Example:</h2>
    <pre>
curl -X POST http://localhost:5000/api/search-ai \\
  -H "Content-Type: application/json" \\
  -d '{{"query": "machine learning"}}'
    </pre>
    
    <h2>Use in n8n:</h2>
    <pre>
HTTP Request node:
- URL: http://localhost:5000/api/search-ai
- Method: POST
- Body: {{"query": "{{{{$json.searchTerm}}}}"}}
    </pre>
    '''

@app.route('/api/save', methods=['POST'])
def api_save():
    try:
        url = request.json.get('url') if request.json else None
        
        # Navigate to URL if provided
        if url:
            subprocess.Popen(['open', url] if sys.platform == 'darwin' else ['xdg-open', url] if sys.platform.startswith('linux') else ['start', url], shell=True)
            time.sleep(3)
        
        save_current_page()
        
        return jsonify({
            'success': True,
            'message': 'Saved to Kinic!',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def api_search():
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'Query required'}), 400
        
        search_kinic(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'message': 'Search completed'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search-ai', methods=['POST'])
def api_search_ai():
    """Search and then run AI on the results"""
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'Query required'}), 400
        
        # Check if user wants to extract the response
        extract = request.json.get('extract_response', True)
        
        ai_response = search_and_ai(query, extract_response=extract)
        
        result = {
            'success': True,
            'query': query,
            'message': 'Search completed and AI analysis triggered'
        }
        
        if ai_response:
            result['ai_response'] = ai_response
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai', methods=['POST'])
def api_ai():
    try:
        click_kinic()
        for _ in range(7):
            pyautogui.press('tab')
            time.sleep(0.2)
        pyautogui.press('enter')
        
        return jsonify({
            'success': True,
            'message': 'AI query triggered'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config/ai-position', methods=['POST'])
def set_ai_position():
    """Set the position where AI responses appear"""
    try:
        data = request.json
        if 'x' in data and 'y' in data:
            config['ai_response_x'] = data['x']
            config['ai_response_y'] = data['y']
            
            # Save to file
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
            
            return jsonify({
                'success': True,
                'message': f'AI response position set to ({data["x"]}, {data["y"]})'
            })
        else:
            return jsonify({'error': 'x and y coordinates required'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n✨ KINIC API")
    print("="*40)
    print(f"✅ Running at: http://localhost:5000")
    print(f"📍 Kinic icon: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print("\n🌐 Open http://localhost:5000 in your browser")
    print("📝 API Docs: http://localhost:5000")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)