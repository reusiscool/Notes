from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram import Dispatcher

from tg.keyboards import start_key, notes_key, cancel_key
from tg.calls import register, login, set_tg_id
from tg.states import FSMRegister, FSMLogin


async def register_index(message: types.Message):
    await message.reply('Enter your username', reply_markup=cancel_key)
    await FSMRegister.name.set()


async def login_index(message: types.Message):
    await message.reply('Enter your username', reply_markup=cancel_key)
    await FSMLogin.name.set()


async def register_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMRegister.next()
    await message.reply('Password ->', reply_markup=cancel_key)


async def login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMLogin.next()
    await message.reply('Password ->', reply_markup=cancel_key)


async def register_password(message: types.Message, state: FSMContext):
    password = message.text
    tg_id = message.from_user.id
    async with state.proxy() as data:
        username = data['username']
    await state.finish()
    req = register(username, password)
    if req['status'] == 'failed':
        await message.reply(req['error'], reply_markup=start_key)
        return
    set_req = set_tg_id(tg_id, req['id'])
    if set_req['status'] == 'failed':
        await message.reply(req['error'], reply_markup=start_key)
    else:
        await message.reply('You have registered.', reply_markup=notes_key)


async def login_password(message: types.Message, state: FSMContext):
    password = message.text
    tg_id = message.from_user.id
    async with state.proxy() as data:
        username = data['username']
    await state.finish()
    req = login(username, password)
    if req['status'] == 'failed':
        await message.reply(req['error'], reply_markup=start_key)
        return
    set_req = set_tg_id(tg_id, req['id'])
    if set_req['status'] == 'failed':
        await message.reply(req['error'], reply_markup=start_key)
    else:
        await message.reply(f'Welcome back, {username}.', reply_markup=notes_key)


async def logout(message: types.Message):
    tg_id = message.from_user.id
    set_req = set_tg_id(tg_id, None)
    if set_req['status'] == 'failed':
        await message.reply(set_req['error'])
    else:
        await message.reply("You have logged out.", reply_markup=start_key)


def register_auth(dp: Dispatcher):
    dp.register_message_handler(register_index, commands=['Register'])
    dp.register_message_handler(login_index, commands=['Login'])
    dp.register_message_handler(register_name, state=FSMRegister.name)
    dp.register_message_handler(login_name, state=FSMLogin.name)
    dp.register_message_handler(register_password, state=FSMRegister.password)
    dp.register_message_handler(login_password, state=FSMLogin.password)
    dp.register_message_handler(logout, commands=['Logout'])
