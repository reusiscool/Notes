from flask import Blueprint, flash, g, request, redirect, render_template, url_for, session
from werkzeug.exceptions import abort
import requests

from auth import login_required
from models import Note

bp = Blueprint("notes", __name__)


@bp.route("/")
@login_required
def index():
    """Show all the posts, most recent first."""
    user_id = session.get('user_id')
    posts = requests.get(request.url_root + url_for('rest.get_all_notes', user_id=user_id)).json()
    return render_template("notes/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.create_note'),
                             json={'title': request.form["title"],
                                   'body': request.form["body"],
                                   'user_id': session.get('user_id')}).json()

        if info['status'] == 'failed':
            flash(info['error'])
        else:
            return redirect(url_for("notes.index"))

    return render_template("notes/create.html")


@bp.route("/<int:id_>/update", methods=("GET", "POST"))
@login_required
def update(id_):
    """Update a post if the current user is the author."""
    note = requests.get(request.url_root + url_for('rest.get_note', note_id=id_)).json()
    if note is None:
        abort(404, f"Note id {id_} doesn't exist.")
    if note['author_id'] != g.user.id():
        abort(403)

    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.update_note', note_id=note['id']),
                             json={'title': request.form["title"], 'body': request.form["body"]}).json()

        if info['status'] == 'failed':
            flash(info['error'])
        else:
            return redirect(url_for("notes.index"))

    return render_template("notes/update.html", note=note)


@bp.route("/<int:id_>/delete", methods=("POST",))
@login_required
def delete(id_):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = Note.with_id(id_)
    if post is None:
        abort(404, f"Post id {id_} doesn't exist.")
    if post.author().id() != g.user.id():
        abort(403)
    post.delete()
    return redirect(url_for("notes.index"))
