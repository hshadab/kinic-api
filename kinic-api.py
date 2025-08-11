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
        print("\nExecuting /save endpoint...")
        
        # Step 1: Focus on Chrome (click somewhere safe on page)
        print("1. Focusing Chrome...")
        pyautogui.click(500, 500)  # Click in safe area to focus Chrome
        time.sleep(1)
        
        # Step 2: Press ESC to close any existing Kinic popup
        print("2. Closing any existing popup (ESC)...")
        pyautogui.press('esc')
        time.sleep(2)
        
        # Step 3: Click Kinic button to open extension
        print(f"3. Opening Kinic at ({config['kinic_x']}, {config['kinic_y']})...")
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)  # Wait for Kinic to fully open
        
        # Step 4: SHIFT+TAB to go to save button
        print("4. Navigating to Save button (SHIFT+TAB)...")
        pyautogui.hotkey('shift', 'tab')
        time.sleep(1)
        
        # Step 5: Press Enter to save
        print("5. Saving page (ENTER)...")
        pyautogui.press('enter')
        time.sleep(3)  # Wait for save to complete
        
        # Step 6: Close Kinic
        print("6. Closing Kinic (ESC)...")
        pyautogui.press('esc')
        time.sleep(1)
        
        print("✓ Page saved successfully")
        return jsonify({'success': True, 'message': 'Page saved to Kinic'})
    except Exception as e:
        print(f"✗ Save failed: {e}")
        pyautogui.press('esc')  # Try to close on error
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search-and-retrieve', methods=['POST'])
def search_and_retrieve():
    """Search Kinic and get first URL"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        print(f"\nExecuting /search-and-retrieve for: '{query}'...")
        
        # Step 1: Focus on Chrome
        print("1. Focusing Chrome...")
        pyautogui.click(500, 500)  # Click in safe area to focus Chrome
        time.sleep(1)
        
        # Step 2: Press ESC to close any existing Kinic popup
        print("2. Closing any existing popup (ESC)...")
        pyautogui.press('esc')
        time.sleep(2)
        
        # Step 3: Click Kinic button to open extension
        print(f"3. Opening Kinic at ({config['kinic_x']}, {config['kinic_y']})...")
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Step 4: Tab to search field
        print("4. Navigating to search field (TAB x4)...")
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        # Step 5: Type query and search
        print(f"5. Typing query: '{query}'...")
        pyautogui.typewrite(query)
        time.sleep(1)
        pyautogui.press('enter')
        
        # Step 6: Wait for results
        print("6. Waiting for search results...")
        time.sleep(4)
        
        # Step 7: Tab to first result
        print("7. Navigating to first result (TAB x2)...")
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(1)
        
        # Step 8: Right-click for context menu
        print("8. Opening context menu (SHIFT+F10)...")
        pyautogui.hotkey('shift', 'f10')
        time.sleep(2)
        
        # Step 9: Navigate to copy URL
        print("9. Navigating to 'Copy link address' (DOWN x5)...")
        for _ in range(5):
            pyautogui.press('down')
            time.sleep(0.3)
        
        print("10. Copying URL (ENTER)...")
        pyautogui.press('enter')
        time.sleep(1)
        
        # Step 10: Get URL from clipboard
        url = pyperclip.paste()
        print(f"11. URL copied: {url[:50]}..." if url else "11. No URL found")
        
        # Step 11: Close Kinic
        print("12. Closing Kinic (ESC)...")
        pyautogui.press('esc')
        time.sleep(1)
        
        print("✓ Search and retrieve completed")
        return jsonify({
            'success': bool(url),
            'query': query,
            'url': url,
            'message': f'Retrieved first URL for: {query}' if url else 'No URL found'
        })
        
    except Exception as e:
        print(f"✗ Search failed: {e}")
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
        
        print(f"\nExecuting /search-ai-extract for: '{query}'...")
        print(f"AI Response position: ({config['ai_response_x']}, {config['ai_response_y']})")
        
        # Step 1: Focus on Chrome
        print("1. Focusing Chrome...")
        pyautogui.click(500, 500)  # Click in safe area to focus Chrome
        time.sleep(1)
        
        # Step 2: Press ESC to close any existing Kinic popup
        print("2. Closing any existing popup (ESC)...")
        pyautogui.press('esc')
        time.sleep(2)
        
        # Step 3: Click Kinic button to open extension
        print(f"3. Opening Kinic at ({config['kinic_x']}, {config['kinic_y']})...")
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        # Step 4: Tab to search field
        print("4. Navigating to search field (TAB x4)...")
        for i in range(4):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        # Step 5: Type search query
        print(f"5. Typing query: '{query}'...")
        pyautogui.typewrite(query)
        time.sleep(2)
        pyautogui.press('enter')
        
        # Step 6: Wait for search results
        print("6. Waiting for search results...")
        time.sleep(4)
        
        # Step 7: Tab to AI button
        print("7. Navigating to AI button (TAB x5)...")
        for i in range(5):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        # Step 8: Click AI button
        print("8. Clicking AI button (ENTER)...")
        pyautogui.press('enter')
        
        # Step 9: Wait for AI response to generate
        print("9. Waiting for AI response generation (10 seconds)...")
        time.sleep(10)
        
        # Step 10: Move to AI response area
        print(f"10. Moving to AI response area ({config['ai_response_x']}, {config['ai_response_y']})...")
        pyautogui.moveTo(config['ai_response_x'], config['ai_response_y'])
        time.sleep(1)
        
        # Step 11: Triple-click to select all text
        print("11. Triple-clicking to select AI text...")
        pyautogui.tripleClick(config['ai_response_x'], config['ai_response_y'])
        time.sleep(2)
        
        # Step 12: Copy to clipboard
        print("12. Copying selected text (CTRL+C)...")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(2)
        
        # Step 13: Get AI response from clipboard
        ai_response = pyperclip.paste()
        print(f"13. Text copied: {len(ai_response)} characters")
        
        # Step 14: Close Kinic
        print("14. Closing Kinic (ESC)...")
        pyautogui.press('esc')
        time.sleep(1)
        
        print("✓ AI extraction completed")
        print(f"   Extracted {len(ai_response)} characters")
        
        return jsonify({
            'success': bool(ai_response),
            'query': query,
            'ai_response': ai_response,
            'message': f'AI response extracted for: {query}' if ai_response else 'No AI response captured'
        })
        
    except Exception as e:
        print(f"✗ AI extraction failed: {e}")
        pyautogui.press('esc')  # Try to close on error
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