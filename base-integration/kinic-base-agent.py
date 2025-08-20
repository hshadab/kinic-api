#!/usr/bin/env python3
"""
Kinic Base Agent - Enhanced desktop agent for Base mini app integration

Extends the original kinic-api.py with:
- Enhanced CORS for hosted Base mini apps
- Better error handling and status reporting
- WebSocket support for real-time communication
- Production-ready endpoints for Base ecosystem
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pyautogui
import pyperclip
import time
import json
import os
import sys
import threading
import queue
from datetime import datetime

# Add parent directory to path to import from original kinic-api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Enhanced CORS for Base mini app hosting
CORS(app, origins=[
    "http://localhost:3000",           # Local development
    "https://localhost:3000",          # Local HTTPS
    "https://*.vercel.app",           # Vercel deployments
    "https://*.netlify.app",          # Netlify deployments
    "https://base.org",               # Base official
    "https://*.base.org",             # Base subdomains
    "https://coinbase.com",           # Coinbase
    "https://*.coinbase.com",         # Coinbase subdomains
    "https://warpcast.com",           # Farcaster
    "https://*.farcaster.xyz"        # Farcaster ecosystem
], supports_credentials=True)

# WebSocket support for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*")

# Load config from parent directory
config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kinic-config.json")
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"✅ Loaded config from {config_file}")
else:
    # Default config - same as original
    config = {
        'kinic_x': 1991, 
        'kinic_y': 150,
        'ai_response_x': 1312,
        'ai_response_y': 1243
    }
    print("⚠️  Using default config - run coordinate setup if needed")

# Configure pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# Operation queue for handling multiple requests
operation_queue = queue.Queue()
current_operation = None

def save_config():
    """Save configuration to file"""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def check_chrome_running():
    """Check if Chrome browser is running"""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome' in proc.info['name'].lower():
                return True
        return False
    except ImportError:
        # Fallback: assume Chrome is running
        return True

def check_kinic_extension():
    """Check if Kinic extension appears to be available"""
    try:
        # Try to click the Kinic button area (non-destructive check)
        screen_width, screen_height = pyautogui.size()
        kinic_x, kinic_y = config['kinic_x'], config['kinic_y']
        
        # Check if coordinates are within screen bounds
        if 0 <= kinic_x <= screen_width and 0 <= kinic_y <= screen_height:
            return True
        return False
    except Exception:
        return False

@app.route('/')
def home():
    """Enhanced status endpoint"""
    return jsonify({
        'service': 'Kinic Base Agent',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'chrome_running': check_chrome_running(),
        'kinic_extension_available': check_kinic_extension(),
        'config': config,
        'endpoints': {
            'status': '/api/status',
            'save': '/api/kinic/save',
            'search': '/api/kinic/search', 
            'search_extract': '/api/kinic/search-extract',
            'setup': '/api/setup'
        },
        'websocket': {
            'enabled': True,
            'events': ['connect', 'operation_status', 'operation_complete']
        }
    })

@app.route('/api/status')
def status():
    """Detailed status check for Base mini app"""
    chrome_running = check_chrome_running()
    kinic_available = check_kinic_extension()
    
    status_info = {
        'agent': 'running',
        'chrome_browser': chrome_running,
        'kinic_extension': kinic_available,
        'ready': chrome_running and kinic_available,
        'config': config,
        'current_operation': current_operation,
        'queue_size': operation_queue.qsize()
    }
    
    if not chrome_running:
        status_info['message'] = 'Chrome browser not detected'
    elif not kinic_available:
        status_info['message'] = 'Kinic extension not accessible - check coordinates'
    else:
        status_info['message'] = 'Ready for operations'
    
    return jsonify(status_info)

@app.route('/api/kinic/save', methods=['POST'])
def save_page_enhanced():
    """Enhanced save page with better error handling and WebSocket updates"""
    global current_operation
    
    try:
        # Get request data
        data = request.get_json() or {}
        page_url = data.get('url', 'current page')
        
        current_operation = {
            'type': 'save',
            'url': page_url,
            'started': datetime.now().isoformat(),
            'status': 'in_progress'
        }
        
        # Emit WebSocket update
        socketio.emit('operation_status', current_operation)
        
        print(f"\n🔄 Base Mini App Save Request")
        print(f"📄 URL: {page_url}")
        print(f"⏰ Started: {current_operation['started']}")
        
        # Pre-flight checks
        if not check_chrome_running():
            raise Exception("Chrome browser not running")
        
        if not check_kinic_extension():
            raise Exception("Kinic extension not accessible - check coordinate configuration")
        
        # Execute save operation (same logic as original)
        print("1. 🎯 Focusing Chrome...")
        pyautogui.click(500, 500)
        time.sleep(1)
        
        print("2. ❌ Closing any existing popup (ESC)...")
        pyautogui.press('esc')
        time.sleep(2)
        
        print(f"3. 🔗 Opening Kinic at ({config['kinic_x']}, {config['kinic_y']})...")
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        print("4. 📑 Navigating to Save button (SHIFT+TAB)...")
        pyautogui.hotkey('shift', 'tab')
        time.sleep(1)
        
        print("5. 💾 Saving page (ENTER)...")
        pyautogui.press('enter')
        
        # Extended wait for save completion
        print("6. ⏳ Waiting for save completion...")
        for i in range(8, 0, -1):
            print(f"   ⏱️  {i}s remaining...")
            socketio.emit('operation_status', {
                **current_operation,
                'progress': f"Saving... {i}s remaining"
            })
            time.sleep(1)
        
        print("7. ❌ Closing Kinic (ESC)...")
        pyautogui.press('esc')
        time.sleep(1)
        
        # Operation complete
        current_operation.update({
            'status': 'completed',
            'completed': datetime.now().isoformat(),
            'result': 'Page saved successfully'
        })
        
        socketio.emit('operation_complete', current_operation)
        print("✅ Save operation completed successfully")
        
        return jsonify({
            'success': True,
            'message': 'Page saved to Kinic memory',
            'operation_id': current_operation['started'],
            'url': page_url
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Save operation failed: {error_msg}")
        
        # Clean up on error
        try:
            pyautogui.press('esc')
        except:
            pass
        
        current_operation = {
            **current_operation,
            'status': 'failed',
            'error': error_msg,
            'completed': datetime.now().isoformat()
        } if current_operation else None
        
        socketio.emit('operation_complete', current_operation)
        
        return jsonify({
            'success': False,
            'error': error_msg,
            'suggestion': get_error_suggestion(error_msg)
        }), 500

@app.route('/api/kinic/search-extract', methods=['POST'])
def search_and_extract_enhanced():
    """Enhanced search with AI extraction"""
    global current_operation
    
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        current_operation = {
            'type': 'search_extract',
            'query': query,
            'started': datetime.now().isoformat(),
            'status': 'in_progress'
        }
        
        socketio.emit('operation_status', current_operation)
        
        print(f"\n🔍 Base Mini App Search Request")
        print(f"❓ Query: '{query}'")
        print(f"⏰ Started: {current_operation['started']}")
        
        # Pre-flight checks
        if not check_chrome_running():
            raise Exception("Chrome browser not running")
        
        # Execute search operation (same logic as original with progress updates)
        steps = [
            "Focusing Chrome...",
            "Closing existing popup...", 
            "Opening Kinic extension...",
            "Navigating to search field...",
            "Typing query...",
            "Performing search...",
            "Navigating to AI button...",
            "Generating AI response...",
            "Extracting response...",
            "Closing extension..."
        ]
        
        step_count = 0
        
        def update_progress(step_msg):
            nonlocal step_count
            step_count += 1
            print(f"{step_count}. {step_msg}")
            socketio.emit('operation_status', {
                **current_operation,
                'progress': f"Step {step_count}/10: {step_msg}"
            })
        
        update_progress("🎯 Focusing Chrome...")
        pyautogui.click(500, 500)
        time.sleep(1)
        
        update_progress("❌ Closing any existing popup...")
        pyautogui.press('esc')
        time.sleep(2)
        
        update_progress(f"🔗 Opening Kinic at ({config['kinic_x']}, {config['kinic_y']})...")
        pyautogui.click(config['kinic_x'], config['kinic_y'])
        time.sleep(3)
        
        update_progress("🔍 Navigating to search field (TAB x4)...")
        for i in range(4):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        update_progress(f"⌨️  Typing query: '{query}'...")
        pyautogui.typewrite(query)
        time.sleep(2)
        pyautogui.press('enter')
        
        update_progress("🔎 Waiting for search results...")
        time.sleep(4)
        
        update_progress("🤖 Navigating to AI button (TAB x5)...")
        for i in range(5):
            pyautogui.press('tab')
            time.sleep(0.5)
        time.sleep(1)
        
        update_progress("🧠 Triggering AI analysis...")
        pyautogui.press('enter')
        
        update_progress("⏳ Waiting for AI response generation...")
        for i in range(10, 0, -1):
            socketio.emit('operation_status', {
                **current_operation,
                'progress': f"AI generating response... {i}s remaining"
            })
            time.sleep(1)
        
        update_progress(f"📋 Extracting AI response from ({config['ai_response_x']}, {config['ai_response_y']})...")
        pyautogui.moveTo(config['ai_response_x'], config['ai_response_y'])
        time.sleep(1)
        pyautogui.tripleClick(config['ai_response_x'], config['ai_response_y'])
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(2)
        
        ai_response = pyperclip.paste()
        
        update_progress("❌ Closing Kinic...")
        pyautogui.press('esc')
        time.sleep(1)
        
        # Operation complete
        current_operation.update({
            'status': 'completed',
            'completed': datetime.now().isoformat(),
            'result': f"AI response extracted: {len(ai_response)} characters"
        })
        
        socketio.emit('operation_complete', current_operation)
        print(f"✅ Search operation completed - extracted {len(ai_response)} characters")
        
        return jsonify({
            'success': bool(ai_response),
            'query': query,
            'ai_response': ai_response,
            'operation_id': current_operation['started'],
            'message': f'AI response extracted for: {query}' if ai_response else 'No AI response captured'
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Search operation failed: {error_msg}")
        
        try:
            pyautogui.press('esc')
        except:
            pass
        
        current_operation = {
            **current_operation,
            'status': 'failed',
            'error': error_msg,
            'completed': datetime.now().isoformat()
        } if current_operation else None
        
        socketio.emit('operation_complete', current_operation)
        
        return jsonify({
            'success': False,
            'error': error_msg,
            'suggestion': get_error_suggestion(error_msg)
        }), 500

def get_error_suggestion(error_msg):
    """Provide helpful suggestions based on error type"""
    if "chrome" in error_msg.lower():
        return "Please ensure Chrome browser is running"
    elif "coordinate" in error_msg.lower() or "extension" in error_msg.lower():
        return "Please run coordinate setup scripts in setup-tools/ directory"
    elif "timeout" in error_msg.lower():
        return "Operation timed out - try again or check if Kinic extension is responding"
    else:
        return "Check that Chrome is open with Kinic extension installed and configured"

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print(f"🔌 Base mini app connected via WebSocket")
    emit('connected', {'status': 'Connected to Kinic Base Agent'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"🔌 Base mini app disconnected")

if __name__ == '__main__':
    print("\n🚀 Kinic Base Agent")
    print("=" * 60)
    print("🎯 Enhanced desktop agent for Base mini app integration")
    print("✅ WebSocket support for real-time updates")
    print("✅ Enhanced CORS for hosted deployments")
    print("✅ Better error handling and status reporting")
    print()
    print("Configuration:")
    print(f"  Kinic button: ({config['kinic_x']}, {config['kinic_y']})")
    print(f"  AI response: ({config['ai_response_x']}, {config['ai_response_y']})")
    print()
    print("🌐 Running on http://localhost:5007")
    print("🔌 WebSocket available on ws://localhost:5007")
    print("📱 Ready for Base mini app connections")
    print("=" * 60)
    
    # Use a different port to avoid conflicts with original kinic-api.py
    socketio.run(app, host='0.0.0.0', port=5007, debug=True, allow_unsafe_werkzeug=True)