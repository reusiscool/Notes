import functools
import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.register'),
                             json={'username': request.form["username"], 'password': request.form["password"]}).json()
        if info['status'] == 'successful':
            session.clear()
            session['user_id'] = info['user_id']
            return redirect(url_for("notes.index"))
        else:
            error = info['error']
        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.login'),
                             json={'username': request.form["username"], 'password': request.form["password"]}).json()

        if info['status'] == 'successful':
            session.clear()
            session["user_id"] = info['id']
            return redirect(url_for("notes.index"))

        flash(info['error'])

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("auth.register"))
