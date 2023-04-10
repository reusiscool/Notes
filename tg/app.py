from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg.init import create_bot, create_dp
from tg.keyboards import start_key, notes_key
from tg.calls import get_user

bot = create_bot()


async def index(message: types.Message):
    user_id = message.from_user.id
    data = get_user(user_id)
    if data['status'] == 'failed':
        await bot.send_message(user_id, '*WELCOME MESSAGE*', reply_markup=start_key)
    else:
        await bot.send_message(user_id, f'You are logged in as {data["username"]}', reply_markup=notes_key)


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    data = get_user(message.from_user.id)
    if data['status'] == 'failed':
        await message.reply('Cancelled', reply_markup=start_key)
    else:
        await message.reply('Cancelled', reply_markup=notes_key)


def register_app(dp: Dispatcher):
    dp.register_message_handler(index, commands=['start'])
    dp.register_message_handler(cancel, commands=['cancel'], state='*')
