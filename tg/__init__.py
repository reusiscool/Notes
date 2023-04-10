from aiogram.utils import executor

from tg.app import register_app
from tg.auth import register_auth
from tg.init import create_dp
from tg.notes import register_notes
from tg.notifications import on_startup


def run():
    dp = create_dp()
    register_app(dp)
    register_auth(dp)
    register_notes(dp)
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)


__all__ = ['run']
