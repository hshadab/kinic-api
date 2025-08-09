#!/usr/bin/env python3
"""Simple Kinic API Server - Control Kinic via HTTP requests"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Disable pyautogui failsafe
pyautogui.FAILSAFE = False

# Load or set default config
config_file = os.path.expanduser("~/.kinic/config.json")
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    # Default position - update if needed
    config = {'kinic_x': 633, 'kinic_y': 413}

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'endpoints': {
            'GET /': 'This help message',
            'POST /click': 'Click the Kinic icon',
            'POST /save': 'Save current page to Kinic',
            'POST /search': 'Search in Kinic (body: {"query": "your search"})',
            'POST /ai': 'Search and run AI (body: {"query": "your search"})',
            'GET /config': 'Get current config',
            'POST /config': 'Update config (body: {"kinic_x": 633, "kinic_y": 413})'
        }
    })

@app.route('/click', methods=['POST'])
def click_kinic():
    """Just click the Kinic icon"""
    try:
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(1)
        return jsonify({'success': True, 'message': f"Clicked at ({config['kinic_x']}, {config['kinic_y']})"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
    """Save the current page to Kinic"""
    try:
        # Click Kinic
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Shift+Tab then Enter to save
        pyautogui.hotkey('shift', 'tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        return jsonify({'success': True, 'message': 'Page saved to Kinic'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_kinic():
    """Search in Kinic"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Click Kinic
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Tab to search field (4 times)
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # Type query and search
        pyautogui.typewrite(query)
        pyautogui.press('enter')
        
        return jsonify({'success': True, 'message': f'Searched for: {query}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/ai', methods=['POST'])
def search_and_ai():
    """Search in Kinic and run AI on results"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Click Kinic
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Tab to search field (4 times)
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # Type query and search
        pyautogui.typewrite(query)
        pyautogui.press('enter')
        
        # Wait for search results
        time.sleep(3)
        
        # Tab 5 more times to AI button and click
        for _ in range(5):
            pyautogui.press('tab')
            time.sleep(0.2)
        pyautogui.press('enter')
        
        return jsonify({'success': True, 'message': f'Searched and AI processing: {query}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify(config)

@app.route('/config', methods=['POST'])
def update_config():
    """Update Kinic position"""
    global config
    try:
        data = request.get_json() or {}
        
        if 'kinic_x' in data:
            config['kinic_x'] = data['kinic_x']
        if 'kinic_y' in data:
            config['kinic_y'] = data['kinic_y']
        
        # Save to file
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic API Server")
    print("=" * 40)
    print(f"Config: Kinic at ({config['kinic_x']}, {config['kinic_y']})")
    print("\nStarting server on http://localhost:5000")
    print("\nExample commands:")
    print('  curl -X POST http://localhost:5000/click')
    print('  curl -X POST http://localhost:5000/save')
    print('  curl -X POST http://localhost:5000/search -H "Content-Type: application/json" -d \'{"query":"python tutorial"}\'')
    print('  curl -X POST http://localhost:5000/ai -H "Content-Type: application/json" -d \'{"query":"explain quantum computing"}\'')
    print("\nPress Ctrl+C to stop")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=False)