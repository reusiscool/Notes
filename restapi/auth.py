from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

from restapi.models import User, UserAlreadyExists

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('POST',))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    data = request.json
    username = data["username"]
    password = data["password"]
    error = ''
    status = 'successful'
    user = None

    if not username:
        error = "Username is required."
        status = 'failed'
    elif not password:
        error = "Password is required."
        status = 'failed'
    if not error:
        try:
            user = User.register(username, generate_password_hash(password))
        except UserAlreadyExists:
            error = f"User {data['username']} is already registered."
            status = 'failed'
    return {'status': status, 'error': error, 'id': user.id() if user else ''}


@bp.route('/login', methods=('POST',))
def login():
    """Log in a registered user by adding the user id to the session."""
    data = request.json
    username = data["username"]
    password = data["password"]
    error = ''
    user = User.with_username(username)

    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(user.password_hash(), password):
        error = "Incorrect password."
    status = 'failed' if error else 'successful'
    return {'status': status, 'error': error, 'id': user.id() if not error else ''}
