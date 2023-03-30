from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="flask.sql",
    )

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    import db
    import notes
    import rest
    import auth

    db.init_app(app)
    app.register_blueprint(rest.bp, url_prefix='/rest')
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(notes.bp)

    return app
