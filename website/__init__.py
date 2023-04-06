import os
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join("website", "flask.sql"),
        API_ROOT='http://127.0.0.1:5000'
    )

    from .notes import bp as note_bp
    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(note_bp)

    return app


