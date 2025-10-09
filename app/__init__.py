import os
from flask import Flask, jsonify
from app.models import db
from app.routes import api
from app.config import config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # ✅ สร้าง Flask app ก่อน
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # ✅ Initialize extensions
    db.init_app(app)

    # ✅ Setup limiter (จำกัดจำนวน request)
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    limiter.init_app(app)

    # ✅ Setup database migration
    migrate = Migrate(app, db)

    # ✅ Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    # ✅ Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Flask Todo API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'todos': '/api/todos'
            }
        })

    # ✅ Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

    # ✅ สร้างตารางถ้ายังไม่มี
    with app.app_context():
        db.create_all()

    return app
