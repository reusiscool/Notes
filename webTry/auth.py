import functools
import requests
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.with_id(user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.register'),
                             json={'username': request.form["username"], 'password': request.form["password"]}).json()
        if info['status'] == 'successful':
            return redirect(url_for("auth.login"))
        else:
            error = info['error']
        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        info = requests.post(request.url_root + url_for('rest.login'),
                             json={'username': request.form["username"], 'password': request.form["password"]}).json()

        if info['status'] == 'successful':
            # store the user id in a new session and return to the index
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
