from flask import Blueprint, request

from .models import User

bp = Blueprint('tg', __name__)


@bp.route('/<int:tg_id>')
def get_user_from_tg(tg_id):
    user = User.with_telegram_id(tg_id)
    if user is None:
        return {'status': 'failed', 'error': 'no such user'}
    d = user.to_json()
    d['status'] = 'successful'
    return d


@bp.route('/<int:tg_id>', methods=("POST",))
def set_user_tg_id(tg_id):
    data = request.json
    user_id = data['user_id']
    if user_id is None:
        User.reset_tg_id(tg_id)
        return {'status': 'successful'}
    user = User.with_id(user_id)
    error = ''
    if user is None:
        error = 'no such user'
    else:
        user.set_tg_id(tg_id)
    return {'status': 'failed' if error else 'successful', 'error': error}

