import os
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join("restapi", "flask.sql"),
    )

    from .db import init_app
    from .user import bp as user_bp
    from .auth import bp as auth_bp
    from .admin import bp as admin_bp
    from .notes import bp as notes_bp

    init_app(app)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(notes_bp, url_prefix='/notes')

    return app


__all__ = ['create_app']
