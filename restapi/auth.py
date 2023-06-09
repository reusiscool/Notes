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


@bp.route('/password', methods=('POST',))
def password_change():
    data = request.json
    user_id = data['user_id']
    old = data['old_password']
    new = data['new_password']
    user = User.with_id(user_id)
    error = ''
    if user is None:
        error = 'No such user'
    else:
        if not check_password_hash(user.password_hash(), old):
            error = 'Wrong password'
        else:
            user.set_password(generate_password_hash(new))
    return {'status': 'failed' if error else 'successful', 'error': error}


@bp.route('/<int:id_>', methods=("POST",))
def delete_user(id_):
    data = request.json
    error = ''
    user = User.with_id(id_)
    if user is None:
        error = 'NO SUCH USER'
    elif not check_password_hash(user.password_hash(), data['password']):
        error = 'NO PERMISSION'
    else:
        user.delete()
    return {"status": "failed" if error else "successful", "error": error}


@bp.route('/user/<int:id_>')
def get_user(id_):
    user = User.with_id(id_)
    if user is None:
        error = 'No such user'
        d = {}
    else:
        error = ''
        d = user.to_json()
    d['status'] = 'failed' if error else 'successful'
    d['error'] = error
    return d
