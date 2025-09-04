from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from anthropic import Anthropic
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
        elif platform == 'perplexity':
            return test_perplexity_connection(api_key, model)
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
        
    except Exception as e:
        error_str = str(e)
        if 'authentication' in error_str.lower() or 'api key' in error_str.lower():
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

def test_perplexity_connection(api_key, model):
    """Test Perplexity API connection (uses OpenAI client)"""
    try:
        # Perplexity uses OpenAI-compatible API
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
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
            'message': 'Perplexity connection successful',
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)