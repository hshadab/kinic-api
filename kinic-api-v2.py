#!/usr/bin/env python3
"""Kinic API v2 - Complete automation with setup and actions"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import pyperclip
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Disable pyautogui failsafe
pyautogui.FAILSAFE = False

# Load or create config
config_file = os.path.expanduser("~/.kinic/config.json")
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    config = {
        'kinic_x': None,
        'kinic_y': None,
        'ai_response_x': None,
        'ai_response_y': None
    }

def save_config():
    """Save config to file"""
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'config': config,
        'setup_endpoints': {
            'POST /setup/kinic-position': 'Set Kinic button position - Body: {"x": 633, "y": 413}',
            'POST /setup/ai-response-position': 'Set AI response text position - Body: {"x": 633, "y": 500}'
        },
        'action_endpoints': {
            'POST /action/save': 'Save current page to Kinic',
            'POST /action/search': 'Search in Kinic - Body: {"query": "your search"}',
            'POST /action/ai-search': 'Search + AI + Copy response - Body: {"query": "your search"}'
        },
        'test_endpoints': {
            'POST /test/click-kinic': 'Test click at Kinic position',
            'POST /test/click-ai-response': 'Test click at AI response position'
        }
    })

# ============= SETUP ENDPOINTS =============

@app.route('/setup/kinic-position', methods=['POST'])
def setup_kinic_position():
    """Set the position of the Kinic button"""
    try:
        data = request.get_json()
        if not data or 'x' not in data or 'y' not in data:
            return jsonify({
                'success': False, 
                'error': 'Please provide x and y coordinates',
                'example': '{"x": 633, "y": 413}'
            }), 400
        
        config['kinic_x'] = data['x']
        config['kinic_y'] = data['y']
        save_config()
        
        return jsonify({
            'success': True,
            'message': f'Kinic button position set to ({data["x"]}, {data["y"]})',
            'config': config
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup/ai-response-position', methods=['POST'])
def setup_ai_response_position():
    """Set the position where AI response text appears"""
    try:
        data = request.get_json()
        if not data or 'x' not in data or 'y' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide x and y coordinates',
                'example': '{"x": 633, "y": 500}'
            }), 400
        
        config['ai_response_x'] = data['x']
        config['ai_response_y'] = data['y']
        save_config()
        
        return jsonify({
            'success': True,
            'message': f'AI response position set to ({data["x"]}, {data["y"]})',
            'config': config
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= ACTION ENDPOINTS =============

@app.route('/action/save', methods=['POST'])
def action_save():
    """Save current page to Kinic"""
    try:
        if not config.get('kinic_x') or not config.get('kinic_y'):
            return jsonify({
                'success': False,
                'error': 'Kinic position not set. Use /setup/kinic-position first'
            }), 400
        
        # Click Kinic button
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)  # Wait for Kinic to open
        
        # Shift+Tab then Enter to save
        pyautogui.hotkey('shift', 'tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        return jsonify({
            'success': True,
            'message': 'Page saved to Kinic'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/action/search', methods=['POST'])
def action_search():
    """Search in Kinic"""
    try:
        if not config.get('kinic_x') or not config.get('kinic_y'):
            return jsonify({
                'success': False,
                'error': 'Kinic position not set. Use /setup/kinic-position first'
            }), 400
        
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide a search query',
                'example': '{"query": "python tutorial"}'
            }), 400
        
        query = data['query']
        
        # Click Kinic button
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)  # Wait for Kinic to open
        
        # Tab to search field (4 times)
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # Type query and search
        pyautogui.typewrite(query)
        pyautogui.press('enter')
        
        return jsonify({
            'success': True,
            'message': f'Searched for: {query}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/action/ai-search', methods=['POST'])
def action_ai_search():
    """Search in Kinic, run AI, and copy the response"""
    try:
        if not config.get('kinic_x') or not config.get('kinic_y'):
            return jsonify({
                'success': False,
                'error': 'Kinic position not set. Use /setup/kinic-position first'
            }), 400
        
        if not config.get('ai_response_x') or not config.get('ai_response_y'):
            return jsonify({
                'success': False,
                'error': 'AI response position not set. Use /setup/ai-response-position first'
            }), 400
        
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide a search query',
                'example': '{"query": "explain quantum computing"}'
            }), 400
        
        query = data['query']
        
        # Click Kinic button
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(2)  # Wait for Kinic to open
        
        # Tab to search field (4 times)
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # Type query and search
        pyautogui.typewrite(query)
        pyautogui.press('enter')
        
        # Wait for search results
        time.sleep(3)
        
        # Tab to AI button (5 more times) and click
        for _ in range(5):
            pyautogui.press('tab')
            time.sleep(0.2)
        pyautogui.press('enter')
        
        # Wait for AI response to generate (adjust this based on typical response time)
        time.sleep(7)
        
        # Click on AI response area
        pyautogui.click(config['ai_response_x'], config['ai_response_y'])
        time.sleep(0.5)
        
        # Triple-click to select all text
        pyautogui.tripleClick()
        time.sleep(0.5)
        
        # Copy to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        # Get the copied text
        try:
            copied_text = pyperclip.paste()
            return jsonify({
                'success': True,
                'message': f'AI search completed for: {query}',
                'response': copied_text
            })
        except:
            return jsonify({
                'success': True,
                'message': f'AI search completed for: {query}',
                'response': 'Text copied to clipboard (unable to read clipboard content)'
            })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= TEST ENDPOINTS =============

@app.route('/test/click-kinic', methods=['POST'])
def test_click_kinic():
    """Test clicking at Kinic position"""
    try:
        if not config.get('kinic_x') or not config.get('kinic_y'):
            return jsonify({
                'success': False,
                'error': 'Kinic position not set. Use /setup/kinic-position first'
            }), 400
        
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        
        return jsonify({
            'success': True,
            'message': f'Clicked at Kinic position ({config["kinic_x"]}, {config["kinic_y"]})'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test/click-ai-response', methods=['POST'])
def test_click_ai_response():
    """Test clicking at AI response position"""
    try:
        if not config.get('ai_response_x') or not config.get('ai_response_y'):
            return jsonify({
                'success': False,
                'error': 'AI response position not set. Use /setup/ai-response-position first'
            }), 400
        
        pyautogui.click(config['ai_response_x'], config['ai_response_y'])
        
        return jsonify({
            'success': True,
            'message': f'Clicked at AI response position ({config["ai_response_x"]}, {config["ai_response_y"]})'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Kinic API v2 Server")
    print("=" * 60)
    print("Current Configuration:")
    print(f"  Kinic button: ({config.get('kinic_x')}, {config.get('kinic_y')})")
    print(f"  AI response: ({config.get('ai_response_x')}, {config.get('ai_response_y')})")
    print("\n📋 Quick Start Guide:")
    print("-" * 60)
    print("1. SETUP - Configure positions first:")
    print('   curl -X POST http://localhost:5001/setup/kinic-position -H "Content-Type: application/json" -d \'{"x":633,"y":413}\'')
    print('   curl -X POST http://localhost:5001/setup/ai-response-position -H "Content-Type: application/json" -d \'{"x":633,"y":500}\'')
    print("\n2. TEST - Verify positions:")
    print('   curl -X POST http://localhost:5001/test/click-kinic')
    print('   curl -X POST http://localhost:5001/test/click-ai-response')
    print("\n3. USE - Run actions:")
    print('   curl -X POST http://localhost:5001/action/save')
    print('   curl -X POST http://localhost:5001/action/search -H "Content-Type: application/json" -d \'{"query":"python"}\'')
    print('   curl -X POST http://localhost:5001/action/ai-search -H "Content-Type: application/json" -d \'{"query":"explain AI"}\'')
    print("\n🌐 Server running on http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=False)