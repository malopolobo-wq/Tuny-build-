"""API Routes"""

from flask import Blueprint, request, jsonify
from core.orchestrator import orchestrator
from core.exceptions import TUNYException
import asyncio

api_bp = Blueprint('api', __name__)
health_bp = Blueprint('health', __name__)

# Health check
@health_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'TUNY',
        'version': '0.1.0',
        'creator': 'Gaïus Ouarahoun'
    })

# Chat endpoint
@api_bp.route('/chat', methods=['POST'])
async def chat():
    """
    Main chat endpoint
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        user_id = data.get('user_id', 'anonymous')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Run async orchestrator
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(orchestrator.process_prompt(prompt, user_id))
        loop.close()
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Intent detection endpoint
@api_bp.route('/intent', methods=['POST'])
async def detect_intent():
    """
    Detect user intent
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        intent = loop.run_until_complete(orchestrator.intent_detector.detect(prompt))
        loop.close()
        
        return jsonify({
            'intent': intent,
            'config': orchestrator.intent_detector.get_intent_config(intent)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Code generation endpoint
@api_bp.route('/generate/code', methods=['POST'])
async def generate_code():
    """
    Generate code
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        language = data.get('language', 'python')
        user_id = data.get('user_id', 'anonymous')
        
        response = await orchestrator.process_prompt(prompt, user_id)
        
        return jsonify({
            'success': True,
            'code': response.get('code'),
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# History endpoint
@api_bp.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """
    Get user conversation history
    """
    try:
        history = orchestrator.memory.get_user_history(user_id)
        return jsonify({
            'success': True,
            'user_id': user_id,
            'history': history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
