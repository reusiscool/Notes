from flask import Blueprint, flash, request, redirect, render_template, url_for, session
import requests

from auth import login_required

bp = Blueprint("notes", __name__)


@bp.route("/")
@login_required
def index():
    user_id = session.get('user_id')
    posts = requests.get(request.url_root + url_for('rest.get_all_notes', user_id=user_id)).json()
    return render_template("notes/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
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
    note = requests.get(request.url_root + url_for('rest.get_note', note_id=id_)).json()

    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.update_note', note_id=note['id']),
                             json={
                                 'title': request.form["title"],
                                 'body': request.form["body"],
                                 'author_id': session.get('user_id')
                             }).json()

        if info['status'] == 'failed':
            flash(info['error'])
        else:
            return redirect(url_for("notes.index"))

    return render_template("notes/update.html", note=note)


@bp.route("/<int:id_>/delete", methods=("POST",))
@login_required
def delete(id_):
    info = requests.post(request.url_root + url_for('rest.delete_note'),
                         json={
                             'note_id': id_,
                             'author_id': session.get('user_id')
                         }).json()
    if info['status'] == 'failed':
        flash(info['error'])
    else:
        return redirect(url_for("notes.index"))


@bp.route("/<int:id_>/retrieve", methods=("POST",))
@login_required
def retrieve(id_):
    info = requests.post(request.url_root + url_for('rest.delete_note'),
                         json={
                             'note_id': id_,
                             'author_id': session.get('user_id')
                         }).json()
    if info['status'] == 'failed':
        flash(info['error'])
    else:
        return redirect(url_for("notes.index"))
