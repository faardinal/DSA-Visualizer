"""
Main Flask application for DSA Visualization Execution Engine.
"""
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Ensure the package root is on sys.path so relative imports work
# when gunicorn runs this as `backend.app`
_here = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_here)
if _root not in sys.path:
    sys.path.insert(0, _root)

from backend.routes import execution_bp


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Enable CORS for all origins on /api/* routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1 MB max request
    app.config['JSON_SORT_KEYS'] = False

    if config:
        app.config.update(config)

    app.register_blueprint(execution_bp)

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


# Module-level app instance for WSGI servers that import `backend.app:app`.
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
