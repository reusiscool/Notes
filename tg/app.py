from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import requests
import os

from keyboards import start_key
from auth import register_auth

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def index(message: types.Message):
    user = message.from_user
    data = requests.get(f'http://127.0.0.1:5000/user/tg/{user.id}').json()
    if data['status'] == 'failed':
        await bot.send_message(user.id, user.full_name, reply_markup=start_key)
    else:
        await bot.send_message(user.id, 'Wassap')


if __name__ == '__main__':
    register_auth(dp)
    executor.start_polling(dp)
