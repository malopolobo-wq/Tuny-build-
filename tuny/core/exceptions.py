"""Exception handling"""

from flask import jsonify

class TUNYException(Exception):
    """Base exception for TUNY"""
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class IntentDetectionError(TUNYException):
    """Error detecting user intent"""
    pass

class CodeGenerationError(TUNYException):
    """Error generating code"""
    pass

class OllamaConnectionError(TUNYException):
    """Cannot connect to Ollama"""
    def __init__(self, message="Cannot connect to Ollama"):
        super().__init__(message, 503)

def register_error_handlers(app):
    """
    Register error handlers for the application
    """
    @app.errorhandler(TUNYException)
    def handle_tuny_exception(error):
        response = {
            'success': False,
            'error': error.message,
            'status': error.status_code
        }
        return jsonify(response), error.status_code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        response = {
            'success': False,
            'error': 'Endpoint not found',
            'status': 404
        }
        return jsonify(response), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        response = {
            'success': False,
            'error': 'Internal server error',
            'status': 500
        }
        return jsonify(response), 500
