import requests
from aiogram.dispatcher import FSMContext
from states import FSMRegister
from aiogram import types
from aiogram import Dispatcher


async def register_index(message: types.Message):
    await message.reply('Enter your username')
    await FSMRegister.name.set()


async def register_name(message: types.Message, state: FSMContext):
    await message.reply('Password ->')
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMRegister.next()
    await message.reply('Password ->')


async def register_password(message: types.Message, state: FSMContext):
    password = message.text
    async with state.proxy() as data:
        username = data['username']
    await state.finish()
    req = requests.post('http://127.0.0.1:8000/auth/register', json={
        'password': password,
        'username': username
    }).json()
    if req['status'] == 'failed':
        await message.reply(req['error'])
    else:
        await message.reply('All good man')


def register_dispatcher(dp: Dispatcher):
    dp.register_message_handler(register_index, commands=['Register'])
    dp.register_message_handler(register_name, state=FSMRegister.name)
    dp.register_message_handler(register_password, state=FSMRegister.password)
