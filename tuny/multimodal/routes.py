"""Multimodal API Routes"""

from flask import Blueprint, request, jsonify, send_file
from multimodal.image_generator import ImageGenerator
from multimodal.video_generator import VideoGenerator
from multimodal.audio_generator import AudioGenerator
from multimodal.speech_to_text import SpeechToText
import asyncio
import os

multimodal_bp = Blueprint('multimodal', __name__, url_prefix='/api/multimodal')

# Initialize generators
image_gen = ImageGenerator()
video_gen = VideoGenerator()
audio_gen = AudioGenerator()
speech_to_text = SpeechToText(model_size='base')

# Image Generation
@multimodal_bp.route('/image/generate', methods=['POST'])
async def generate_image():
    """
    Generate image from text prompt
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt', '')
        width = data.get('width', 512)
        height = data.get('height', 512)
        
        if not prompt:
            return jsonify({'error': 'Prompt required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(image_gen.generate(
            prompt, negative_prompt, width=width, height=height
        ))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@multimodal_bp.route('/image/variations', methods=['POST'])
async def generate_image_variations():
    """
    Generate variations of an image
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Image file required'}), 400
        
        image_file = request.files['image']
        num_variations = request.form.get('num_variations', 4, type=int)
        
        # Save temp image
        temp_path = f'/tmp/{image_file.filename}'
        image_file.save(temp_path)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(image_gen.generate_variations(
            temp_path, num_variations
        ))
        loop.close()
        
        os.remove(temp_path)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Video Generation
@multimodal_bp.route('/video/from-image', methods=['POST'])
async def generate_video_from_image():
    """
    Generate video from static image
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Image file required'}), 400
        
        image_file = request.files['image']
        num_frames = request.form.get('num_frames', 25, type=int)
        
        temp_path = f'/tmp/{image_file.filename}'
        image_file.save(temp_path)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(video_gen.generate_from_image(
            temp_path, num_frames
        ))
        loop.close()
        
        os.remove(temp_path)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@multimodal_bp.route('/video/animate', methods=['POST'])
async def generate_animation():
    """
    Generate animation from text
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        num_frames = data.get('num_frames', 60)
        animation_type = data.get('animation_type', 'camera_zoom')
        
        if not prompt:
            return jsonify({'error': 'Prompt required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(video_gen.generate_animation(
            prompt, num_frames, animation_type
        ))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Audio Generation
@multimodal_bp.route('/audio/speech', methods=['POST'])
async def generate_speech():
    """
    Generate speech from text
    """
    try:
        data = request.json
        text = data.get('text')
        voice = data.get('voice', 'default')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'Text required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(audio_gen.generate_speech(
            text, voice, language
        ))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@multimodal_bp.route('/audio/voice-clone', methods=['POST'])
async def voice_clone():
    """
    Generate speech with voice cloning
    """
    try:
        if 'voice_sample' not in request.files:
            return jsonify({'error': 'Voice sample required'}), 400
        
        data = request.form
        text = data.get('text')
        voice_file = request.files['voice_sample']
        
        if not text:
            return jsonify({'error': 'Text required'}), 400
        
        temp_path = f'/tmp/{voice_file.filename}'
        voice_file.save(temp_path)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(audio_gen.voice_clone(
            text, temp_path
        ))
        loop.close()
        
        os.remove(temp_path)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Speech-to-Text
@multimodal_bp.route('/speech-to-text', methods=['POST'])
async def transcribe_audio():
    """
    Transcribe audio to text
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio file required'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', None)
        
        temp_path = f'/tmp/{audio_file.filename}'
        audio_file.save(temp_path)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(speech_to_text.transcribe(
            temp_path, language
        ))
        loop.close()
        
        os.remove(temp_path)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
