import os
from flask import Flask
import dotenv


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    dotenv.load_dotenv()
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join("website", "flask.sql"),
        API_ROOT=os.getenv('API_ROOT')
    )

    from .notes import bp as note_bp
    from .auth import bp as auth_bp
    from .user import bp as user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(note_bp)

    return app
