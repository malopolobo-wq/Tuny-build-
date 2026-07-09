"""Compilation API Routes"""

from flask import Blueprint, request, jsonify, send_file
from compilation.compiler import MultiLanguageCompiler
from compilation.workflow_generator import WorkflowGenerator
import asyncio
import os

compilation_bp = Blueprint('compilation', __name__, url_prefix='/api/compilation')

# Initialize
compiler = MultiLanguageCompiler()
workflow_gen = WorkflowGenerator()

@compilation_bp.route('/compile', methods=['POST'])
async def compile_code():
    """
    Compile code to native binary
    """
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language')
        target_platform = data.get('target_platform', 'linux')
        output_name = data.get('output_name', 'app')
        
        if not code or not language:
            return jsonify({'error': 'Code and language required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler.compile(
            code, language, target_platform, output_name
        ))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/compile/python', methods=['POST'])
async def compile_python():
    """
    Compile Python to executable
    """
    try:
        data = request.json
        code = data.get('code')
        output_name = data.get('output_name', 'app')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler._compile_python(code, output_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/compile/javascript', methods=['POST'])
async def compile_javascript():
    """
    Compile JavaScript to binary
    """
    try:
        data = request.json
        code = data.get('code')
        output_name = data.get('output_name', 'app')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler._compile_javascript(code, output_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/compile/cpp', methods=['POST'])
async def compile_cpp():
    """
    Compile C++ code
    """
    try:
        data = request.json
        code = data.get('code')
        platform = data.get('platform', 'linux')
        output_name = data.get('output_name', 'app')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler._compile_cpp(code, platform, output_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/compile/go', methods=['POST'])
async def compile_go():
    """
    Compile Go code
    """
    try:
        data = request.json
        code = data.get('code')
        platform = data.get('platform', 'linux')
        output_name = data.get('output_name', 'app')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler._compile_go(code, platform, output_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/compile/rust', methods=['POST'])
async def compile_rust():
    """
    Compile Rust code
    """
    try:
        data = request.json
        code = data.get('code')
        platform = data.get('platform', 'linux')
        output_name = data.get('output_name', 'app')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler._compile_rust(code, platform, output_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/mobile/apk', methods=['POST'])
async def generate_apk():
    """
    Generate Android APK
    """
    try:
        data = request.json
        code = data.get('code')
        app_name = data.get('app_name', 'TunyApp')
        package_name = data.get('package_name', 'com.tuny.app')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler.generate_apk(code, app_name, package_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/mobile/ipa', methods=['POST'])
async def generate_ipa():
    """
    Generate iOS IPA
    """
    try:
        data = request.json
        code = data.get('code')
        app_name = data.get('app_name', 'TunyApp')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(compiler.generate_ipa(code, app_name))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/workflow/generate', methods=['POST'])
def generate_workflow():
    """
    Generate GitHub Actions workflow
    """
    try:
        data = request.json
        languages = data.get('languages', ['python', 'javascript'])
        platforms = data.get('platforms', ['linux', 'windows', 'macos'])
        workflow_type = data.get('type', 'compile')  # compile or test
        
        if workflow_type == 'test':
            workflow_content = workflow_gen.generate_test_workflow()
        else:
            workflow_content = workflow_gen.generate_compile_workflow(languages, platforms)
        
        workflow_path = workflow_gen.save_workflow(f'{workflow_type}_workflow', workflow_content)
        
        return jsonify({
            'success': True,
            'workflow': workflow_content,
            'file': workflow_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/binaries', methods=['GET'])
def list_binaries():
    """
    List compiled binaries
    """
    try:
        binaries_dir = 'data/compiled_binaries'
        if not os.path.exists(binaries_dir):
            return jsonify({'binaries': []})
        
        binaries = []
        for root, dirs, files in os.walk(binaries_dir):
            for file in files:
                file_path = os.path.join(root, file)
                binaries.append({
                    'name': file,
                    'path': file_path,
                    'size': os.path.getsize(file_path)
                })
        
        return jsonify({'success': True, 'binaries': binaries})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compilation_bp.route('/download/<filename>', methods=['GET'])
def download_binary(filename):
    """
    Download compiled binary
    """
    try:
        file_path = os.path.join('data/compiled_binaries', filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
