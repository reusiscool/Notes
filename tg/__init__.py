from tg.app import dp
from tg.auth import register_auth
from tg.notes import register_notes


def create_dp():
    register_auth(dp)
    register_notes(dp)
    return dp


__all__ = ['create_dp']
