"""Code Analysis Routes"""

from flask import Blueprint, request, jsonify
from code_analysis.static_analyzer import StaticAnalyzer
from code_analysis.bug_detector import BugDetector
from code_analysis.test_generator import TestGenerator
from code_analysis.code_optimizer import CodeOptimizer
import asyncio

code_analysis_bp = Blueprint('code_analysis', __name__, url_prefix='/api/analysis')

# Initialize analyzers
static_analyzer = StaticAnalyzer()
bug_detector = BugDetector()
test_generator = TestGenerator()
code_optimizer = CodeOptimizer()

@code_analysis_bp.route('/analyze', methods=['POST'])
async def analyze_code():
    """
    Comprehensive code analysis
    """
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run all analyses
        analysis_results = {
            'language': language,
            'code_length': len(code),
            'lines': len(code.split('\n'))
        }
        
        # Static analysis
        if language == 'python':
            static_result = loop.run_until_complete(static_analyzer.analyze_python(code))
            analysis_results['static_analysis'] = static_result
        elif language == 'javascript':
            static_result = loop.run_until_complete(static_analyzer.analyze_javascript(code))
            analysis_results['static_analysis'] = static_result
        
        # Bug detection
        bug_result = loop.run_until_complete(bug_detector.detect(code, language))
        analysis_results['bugs'] = bug_result
        
        # Optimization suggestions
        opt_result = loop.run_until_complete(code_optimizer.optimize(code, language))
        analysis_results['optimizations'] = opt_result
        
        loop.close()
        
        return jsonify({
            'success': True,
            'analysis': analysis_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@code_analysis_bp.route('/static-analysis', methods=['POST'])
async def static_analysis():
    """
    Static code analysis only
    """
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if language == 'python':
            result = loop.run_until_complete(static_analyzer.analyze_python(code))
        elif language == 'javascript':
            result = loop.run_until_complete(static_analyzer.analyze_javascript(code))
        else:
            result = {'error': f'Language {language} not supported'}
        
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@code_analysis_bp.route('/detect-bugs', methods=['POST'])
async def detect_bugs():
    """
    Detect potential bugs
    """
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(bug_detector.detect(code, language))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@code_analysis_bp.route('/generate-tests', methods=['POST'])
async def generate_tests():
    """
    Generate unit tests
    """
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language', 'python')
        framework = data.get('framework', 'auto')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_generator.generate_tests(
            code, language, framework
        ))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@code_analysis_bp.route('/optimize', methods=['POST'])
async def optimize():
    """
    Get optimization suggestions
    """
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(code_optimizer.optimize(code, language))
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
