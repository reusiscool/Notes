from flask import Blueprint, flash, request, redirect, render_template, url_for, session, current_app, abort
import requests

bp = Blueprint('user', __name__, url_prefix="/auth")


@bp.route('/user', methods=('GET', "POST"))
def user_index():
    if request.method == 'POST':
        form = request.form
        if form['action'] == 'Reset':
            if form['new_password']:
                data = requests.post(current_app.config['API_ROOT'] + '/auth/password', json={
                    'user_id': session.get('user_id'),
                    'old_password': form['old_password'],
                    'new_password': form['new_password']
                }).json()
                if data['status'] == 'successful':
                    return redirect(url_for('notes.index'))
                error = data['error']
            else:
                error = 'Enter your new password'

        else:
            data = requests.post(current_app.config['API_ROOT'] + f'/auth/{session.get("user_id")}',
                                 json={'password': form['old_password']}).json()
            if data['status'] == 'successful':
                session.clear()
                return redirect(url_for('auth.index'))
            error = data['error']

        flash(error)
    user_id = session.get('user_id')
    user = requests.get(current_app.config['API_ROOT'] + f'/auth/user/{user_id}').json()
    if user['status'] == 'failed':
        abort(404)
    return render_template('user.html', username=user['username'])
