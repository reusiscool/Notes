from flask import Blueprint, request

from models import User, Note, UserAlreadyExists
from werkzeug.security import generate_password_hash, check_password_hash
from db import init_db

bp = Blueprint('rest', __name__)


@bp.route('/post', methods=("GET",))
def all_posts():
    return Note


@bp.route('/user', methods=('POST',))
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
    return {'status': status, 'error': error, 'user_id': user.id() if user else ''}


@bp.route('/user/login', methods=('POST',))
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
    return {'status': status, 'error': error, 'id': user.id() if user else ''}


@bp.route('/user/<int:id_>')
def get_user(id_):
    return User.with_id(id_).__dict__


@bp.route('/notes/<int:user_id>')
def get_all_notes(user_id):
    """Show all users notes, most recent first."""
    return [{'id': note.id(), 'body': note.body(),
             'title': note.title(), 'created': note.created()}
            for note in Note.with_author_id(user_id) if not note.is_deleted()]


@bp.route('/notes', methods=('POST',))
def create_note():
    """Create a new post for the current user."""
    data = request.json
    title = data["title"]
    body = data["body"]
    user_id = data['user_id']
    error = ''

    if not title:
        error = "Title is required."
    if not error:
        Note.create(title, body, user_id)
    return {'status': 'failed' if error else 'successful', 'error': error}


@bp.route('/note/<int:note_id>')
def get_note(note_id):
    note = Note.with_id(note_id)
    return {'id': note.id(), 'body': note.body(), 'author_id': note.author().id(),
            'title': note.title(), 'created': note.created()}


@bp.route('/note/<int:note_id>', methods=("POST",))
def update_note(note_id):
    """Update a post if the current user is the author."""
    note = Note.with_id(note_id)
    data = request.json
    title = data["title"]
    body = data["body"]
    author_id = data['author_id']
    error = ''

    if not title:
        error = "Title is required."
    elif note.author().id() != author_id:
        error = 'No permission'
    else:
        note.update(title, body)
    return {'status': 'failed' if error else 'successful', 'error': error}


@bp.route('/delete_note', methods=("POST",))
def delete_note():
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    data = request.json
    note = Note.with_id(data['note_id'])
    if not note:
        error = 'No such note'
    elif note.author().id() != data['author_id']:
        error = 'You dont have enough permission'
    else:
        error = ''
        deleted_notes = [n for n in Note.with_author_id(data['author_id']) if n.is_deleted()]
        while len(deleted_notes) >= 10:
            n = deleted_notes.pop()
            n.delete_fr()
        note.delete()
    return {'status': 'failed' if error else 'successful', 'error': error}


@bp.route('/wipe', methods=("POST",))
def reset_db():
    init_db()
    return {}
