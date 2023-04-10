from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os


def create_bot():
    if create_bot.bot is not None:
        return create_bot.bot
    load_dotenv()
    TOKEN = os.getenv('BOT_TOKEN')
    create_bot.bot = Bot(token=TOKEN)
    return create_bot.bot


create_bot.bot = None


def create_dp():
    if create_dp.dp is None:
        b = create_bot()
        create_dp.dp = Dispatcher(bot=b, storage=MemoryStorage())
    return create_dp.dp


create_dp.dp = None
