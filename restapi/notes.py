from flask import Blueprint, request

from restapi.models import Note, User

bp = Blueprint('notes', __name__)


@bp.route('/<int:user_id>')
def get_all_notes(user_id):
    """Show all users notes, most recent first."""
    return [{'id': note.id(), 'body': note.body(),
             'title': note.title(), 'created': note.created()}
            for note in Note.with_author_id(user_id) if not note.is_deleted()]


@bp.route('/deleted/<int:user_id>')
def get_all_deleted_notes(user_id):
    """Show all users deleted notes, most recent first."""
    res = [{'id': note.id(), 'body': note.body(),
            'title': note.title(), 'created': note.created(), 'deleted': note.deleted()}
           for note in Note.with_author_id(user_id) if note.is_deleted()]
    res.sort(key=lambda x: x['deleted'], reverse=True)
    return res


@bp.route('/create', methods=('POST',))
def create_note():
    """Create a new post for the current user."""
    data = request.json
    title = data["title"]
    body = data["body"]
    user_id = data['user_id']
    datetime = data['datetime']
    error = ''

    if not title:
        error = "Title is required."
    elif not User.with_id(user_id):
        error = "NO SUCH USER"
    else:
        Note.create(title, body, user_id, datetime)
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
    elif note is None:
        error = 'No such note'
    elif note.author().id() != author_id:
        error = 'No permission'
    else:
        note.update(title, body)
    return {'status': 'failed' if error else 'successful', 'error': error}


@bp.route('/delete_note', methods=("POST",))
def delete_note():
    """Delete a post.

    Ensures that the post exists and that the logged-in user is the
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
        deleted_notes.sort(key=lambda x: x.deleted(), reverse=True)
        while len(deleted_notes) >= 10:
            n = deleted_notes.pop()
            n.delete_fr()
        note.delete()
    return {'status': 'failed' if error else 'successful', 'error': error}


@bp.route('/restore_note', methods=("POST",))
def restore_note():
    """Restore a post.

    Ensures that the post exists and that the logged-in user is the
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
        note.restore()
    return {'status': 'failed' if error else 'successful', 'error': error}
