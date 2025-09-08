from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from anthropic import Anthropic
try:
    from anthropic import APIStatusError  # normalized error handling
except Exception:  # fallback if SDK changes
    class APIStatusError(Exception):
        pass
import os
from datetime import datetime

app = Flask(__name__)

# Restrictive CORS: allow localhost and optional env overrides
def _allowed_origins():
    default = " ".join([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null",  # allow local file:// testers
    ])
    origins_str = os.environ.get("ALLOWED_ORIGINS", default)
    return [o.strip() for o in origins_str.split() if o.strip()]

CORS(app, resources={r"/api/*": {"origins": _allowed_origins()}})

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test connection to AI platform with provided credentials"""
    try:
        data = request.json
        platform = data.get('platform')
        model = data.get('model')
        api_key = data.get('apiKey')
        
        if not all([platform, model, api_key]):
            return jsonify({
                'success': False,
                'error': 'Missing required parameters'
            }), 400
        
        # Test based on platform
        if platform == 'openai':
            return test_openai_connection(api_key, model)
        elif platform == 'anthropic':
            return test_anthropic_connection(api_key, model)
        elif platform == 'deepseek':
            return test_deepseek_connection(api_key, model)
        elif platform == 'gemini':
            return test_gemini_connection(api_key, model)
        elif platform == 'grok':
            return test_grok_connection(api_key, model)
        else:
            return jsonify({
                'success': False,
                'error': f'Platform {platform} not yet implemented'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def test_openai_connection(api_key, model):
    """Test OpenAI API connection"""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Make a simple test call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Connection successful' in exactly 3 words"}
            ],
            max_tokens=10
        )
        
        return jsonify({
            'success': True,
            'message': 'OpenAI connection successful',
            'response': response.choices[0].message.content,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
        
    except openai.AuthenticationError:
        return jsonify({
            'success': False,
            'error': 'Invalid API key'
        }), 401
    except openai.NotFoundError:
        return jsonify({
            'success': False,
            'error': f'Model {model} not found or not accessible'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def test_anthropic_connection(api_key, model):
    """Test Anthropic API connection"""
    try:
        client = Anthropic(api_key=api_key)
        
        # Make a simple test call
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[
                {"role": "user", "content": "Say 'Connection successful' in exactly 3 words"}
            ]
        )
        
        return jsonify({
            'success': True,
            'message': 'Anthropic connection successful',
            'response': response.content[0].text,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
        
    except APIStatusError as e:
        status = getattr(e, "status_code", None)
        if status in (401, 403):
            return jsonify({'success': False, 'error': 'Invalid API key'}), 401
        if status == 404:
            return jsonify({'success': False, 'error': f'Model {model} not found or not accessible'}), 404
        return jsonify({'success': False, 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def test_deepseek_connection(api_key, model):
    """Test DeepSeek API connection (uses OpenAI client)"""
    try:
        # DeepSeek uses OpenAI-compatible API
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Connection successful' in exactly 3 words"}
            ],
            max_tokens=10
        )
        
        return jsonify({
            'success': True,
            'message': 'DeepSeek connection successful',
            'response': response.choices[0].message.content,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_str = str(e)
        if 'authentication' in error_str.lower() or 'api key' in error_str.lower():
            return jsonify({
                'success': False,
                'error': 'Invalid API key'
            }), 401
        else:
            return jsonify({
                'success': False,
                'error': error_str
            }), 500

def test_gemini_connection(api_key, model):
    """Test Google Gemini API connection"""
    try:
        import google.generativeai as genai
        
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Create the model
        gemini_model = genai.GenerativeModel(model)
        
        # Make a simple test call
        response = gemini_model.generate_content("Say 'Connection successful' in exactly 3 words")
        
        return jsonify({
            'success': True,
            'message': 'Google Gemini connection successful',
            'response': response.text,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_str = str(e)
        if 'api key' in error_str.lower() or 'invalid' in error_str.lower():
            return jsonify({
                'success': False,
                'error': 'Invalid API key'
            }), 401
        elif 'model' in error_str.lower():
            return jsonify({
                'success': False,
                'error': f'Model {model} not found or not accessible'
            }), 404
        else:
            return jsonify({
                'success': False,
                'error': error_str
            }), 500

def test_grok_connection(api_key, model):
    """Test xAI Grok API connection"""
    try:
        # Grok uses OpenAI-compatible API
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Connection successful' in exactly 3 words"}
            ],
            max_tokens=10
        )
        
        return jsonify({
            'success': True,
            'message': 'xAI Grok connection successful',
            'response': response.choices[0].message.content,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_str = str(e)
        if 'authentication' in error_str.lower() or 'api key' in error_str.lower():
            return jsonify({
                'success': False,
                'error': 'Invalid API key - Note: Grok API requires special access'
            }), 401
        else:
            return jsonify({
                'success': False,
                'error': error_str
            }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host=host, port=port)
