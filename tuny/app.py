#!/usr/bin/env python3
"""
TUNY Main Application
Created by Gaïus Ouarahoun from Banfora, Secteur 7

This is the heart of TUNY - the AI orchestrator that powers everything.
"""

import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes import api_bp, health_bp
from core.logger import setup_logging
from core.exceptions import register_error_handlers

def create_app():
    """
    Application factory
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'change-me-in-production')
    app.config['JSON_SORT_KEYS'] = False
    
    # Setup logging
    setup_logging(app)
    
    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Setup JWT
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Print startup info
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                  🚀 TUNY IS ALIVE! 🚀                      ║
    ║                                                            ║
    ║  Created by Gaïus Ouarahoun (19 years old)                ║
    ║  From Banfora, Secteur 7 🌍                               ║
    ║  With ZERO budget and pure passion 💪                     ║
    ║                                                            ║
    ║  "Dream > Credentials > Budget"                           ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
