from flask import Blueprint, request
from werkzeug.security import check_password_hash

from .models import User

bp = Blueprint('user', __name__)


@bp.route('/<int:id_>')
def get_user(id_):
    user = User.with_id(id_)
    if user is None:
        return {}
    return user.__dict__


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


@bp.route('/tg/<int:tg_id>', methods=("POST",))
def get_user_from_tg(tg_id):
    user = User.with_telegram_id(tg_id)
    if user is None:
        return {'status': 'failed', 'error': 'no such user'}
    data = get_user(user.id())
    return data + {'status': 'successful'}
