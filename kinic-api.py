#!/usr/bin/env python3
"""Kinic API - Control Kinic Chrome Extension from your AI"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import pyperclip
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Load config from current directory
config_file = "kinic-config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"Loaded config from {config_file}")
else:
    # Default config
    config = {
        'kinic_x': 1991, 
        'kinic_y': 150,
        'ai_response_x': 1312,
        'ai_response_y': 1243
    }
    print("Using default config")

def save_config():
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

# Configure pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'service': 'Kinic API',
        'config': config,
        'endpoints': [
            '/click',
            '/close', 
            '/save',
            '/search-and-retrieve',
            '/search-ai-extract',
            '/setup-kinic',
            '/setup-ai'
        ]
    })

@app.route('/click', methods=['POST'])
def click_kinic():
    """Click the Kinic button"""
    try:
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        return jsonify({'success': True, 'message': 'Kinic clicked'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/close', methods=['POST'])
def close_kinic():
    """Close Kinic popup"""
    try:
        pyautogui.press('esc')
        return jsonify({'success': True, 'message': 'Kinic closed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_page():
    """Save current page to Kinic"""
    try:
        # Click Kinic
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)
        
        # Tab to save button (assuming it's first or second tab)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)
        
        # Close
        pyautogui.press('esc')
        
        return jsonify({'success': True, 'message': 'Page saved to Kinic'})
    except Exception as e:
        pyautogui.press('esc')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-and-retrieve', methods=['POST'])
def search_and_retrieve():
    """Search Kinic and get first URL"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Close any existing popup
        pyautogui.press('esc')
        time.sleep(1)
        
        # Open Kinic
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Tab to search field
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.5)
        
        # Type query
        pyautogui.typewrite(query)
        time.sleep(1)
        pyautogui.press('enter')
        
        # Wait for results
        time.sleep(4)
        
        # Tab to first result
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(1)
        
        # Right-click for context menu
        pyautogui.hotkey('shift', 'f10')
        time.sleep(2)
        
        # Navigate to copy URL
        for _ in range(5):
            pyautogui.press('down')
            time.sleep(0.3)
        
        pyautogui.press('enter')
        time.sleep(1)
        
        # Get URL from clipboard
        url = pyperclip.paste()
        
        # Close
        pyautogui.press('esc')
        
        return jsonify({
            'success': bool(url),
            'query': query,
            'url': url,
            'message': f'Retrieved first URL for: {query}' if url else 'No URL found'
        })
        
    except Exception as e:
        pyautogui.press('esc')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-ai-extract', methods=['POST'])
def search_ai_extract():
    """Search and extract AI response"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        print(f"\n{'='*60}")
        print(f"Starting AI extraction for query: '{query}'")
        print(f"AI Response position: ({config['ai_response_x']}, {config['ai_response_y']})")
        print(f"{'='*60}\n")
        
        # Close any existing popup
        print("1. Closing any existing popups...")
        pyautogui.press('esc')
        time.sleep(2)
        
        # Open Kinic
        print(f"2. Opening Kinic at ({config['kinic_x']}, {config['kinic_y']})...")
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Tab to search field
        print("3. Navigating to search field...")
        for i in range(4):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        # Type search query
        print(f"4. Typing query: '{query}'...")
        pyautogui.typewrite(query)
        time.sleep(2)
        pyautogui.press('enter')
        
        # Wait for search results
        print("5. Waiting for search results...")
        time.sleep(4)
        
        # Tab to AI button
        print("6. Navigating to AI button...")
        for i in range(5):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        # Click AI button
        print("7. Clicking AI button...")
        pyautogui.press('enter')
        
        # Wait for AI response to generate
        print("8. Waiting for AI response generation...")
        time.sleep(10)
        
        # Move to AI response area
        print(f"9. Moving to AI response area ({config['ai_response_x']}, {config['ai_response_y']})...")
        pyautogui.moveTo(config['ai_response_x'], config['ai_response_y'])
        time.sleep(1)
        
        # Triple-click to select all text
        print("10. Triple-clicking to select AI text...")
        pyautogui.tripleClick(config['ai_response_x'], config['ai_response_y'])
        time.sleep(2)
        
        # Copy to clipboard
        print("11. Copying selected text...")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(2)
        
        # Get AI response from clipboard
        print("12. Reading from clipboard...")
        ai_response = pyperclip.paste()
        
        # Close Kinic
        print("13. Closing Kinic...")
        time.sleep(2)
        pyautogui.press('esc')
        
        print(f"\n{'='*60}")
        print(f"Extraction complete!")
        print(f"Extracted {len(ai_response)} characters")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': bool(ai_response),
            'query': query,
            'ai_response': ai_response,
            'message': f'AI response extracted for: {query}' if ai_response else 'No AI response captured'
        })
        
    except Exception as e:
        print(f"\nError: {e}")
        pyautogui.press('esc')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup-kinic', methods=['POST'])
def setup_kinic():
    """Update Kinic button position"""
    try:
        data = request.get_json() or {}
        config['kinic_x'] = data.get('x', config['kinic_x'])
        config['kinic_y'] = data.get('y', config['kinic_y'])
        save_config()
        
        return jsonify({
            'success': True,
            'kinic_x': config['kinic_x'],
            'kinic_y': config['kinic_y']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup-ai', methods=['POST'])
def setup_ai():
    """Update AI response position"""
    try:
        data = request.get_json() or {}
        config['ai_response_x'] = data.get('x', config['ai_response_x'])
        config['ai_response_y'] = data.get('y', config['ai_response_y'])
        save_config()
        
        return jsonify({
            'success': True,
            'ai_response_x': config['ai_response_x'],
            'ai_response_y': config['ai_response_y']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 Kinic API")
    print("=" * 60)
    print("✅ AI text extraction is now WORKING!")
    print()
    print("Configuration:")
    print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
    print(f"  AI response: ({config['ai_response_x']}, {config['ai_response_y']})")
    print()
    print("Running on http://localhost:5006")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5006)