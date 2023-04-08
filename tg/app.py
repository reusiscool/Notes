from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os

from tg.keyboards import start_key, notes_key
from tg.calls import get_user

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def index(message: types.Message):
    user_id = message.from_user.id
    data = get_user(user_id)
    if data['status'] == 'failed':
        await bot.send_message(user_id, '*WELCOME MESSAGE*', reply_markup=start_key)
    else:
        await bot.send_message(user_id, f'You are logged in as {data["username"]}', reply_markup=notes_key)


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    data = get_user(message.from_user.id)
    if data['status'] == 'failed':
        await message.reply('Cancelled', reply_markup=start_key)
    else:
        await message.reply('Cancelled', reply_markup=notes_key)
