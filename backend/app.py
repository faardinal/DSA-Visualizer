"""
Main Flask application for DSA Visualization Execution Engine.
Phase 3.1: Backend Foundation.
"""
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Handle imports for both direct execution and package imports
try:
    from .routes import execution_bp
except ImportError:
    # Running directly (python app.py), add parent directory to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from backend.routes import execution_bp


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Enable CORS for frontend integration
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB max request
    app.config['JSON_SORT_KEYS'] = False

    if config:
        app.config.update(config)

    # Register blueprints
    app.register_blueprint(execution_bp)

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            "service": "DSA Visualization Execution Engine",
            "version": "1.0.0",
            "endpoints": {
                "health": "GET /api/health",
                "run": "POST /api/run",
                "config": "GET /api/config"
            }
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(413)
    def request_too_large(e):
        return jsonify({"error": "Request too large (max 1MB)"}), 413

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)