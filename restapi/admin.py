from flask import Blueprint

from restapi.db import init_db

bp = Blueprint('admin', __name__)


@bp.route('/wipe', methods=("POST",))
def reset_db():
    init_db()
    return {}