from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg.calls import get_user, get_notes, create
from tg.states import FSMCreate
from tg.keyboards import start_key, notes_key, cancel_key


async def show_notes(message: types.Message):
    tg_id = message.from_user.id
    user_data = get_user(tg_id)
    if user_data['status'] == 'failed':
        await message.reply('You are not logged in', reply_markup=start_key)
        return
    notes_data = get_notes(user_data['id'])
    ls = []
    for note in notes_data:
        ls.append(f'{note["title"]}\n{note["created"]}\n{note["body"]}\n')
    await message.reply('\n'.join(ls), reply_markup=notes_key)


async def create_index(message: types.Message):
    tg_id = message.from_user.id
    user_data = get_user(tg_id)
    if user_data['status'] == 'failed':
        await message.reply('You are not logged in', reply_markup=start_key)
        return
    await FSMCreate.title.set()
    await message.reply('Title ->', reply_markup=cancel_key)


async def create_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await FSMCreate.next()
    await message.reply('Body ->', reply_markup=cancel_key)


async def create_body(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    body = message.text
    async with state.proxy() as data:
        title = data['title']
    await state.finish()
    user_data = get_user(tg_id)
    post_data = create(title, body, user_data['id'])
    if post_data['status'] == 'failed':
        await message.reply(post_data['error'], reply_markup=notes_key)
    else:
        await message.reply('Cool', reply_markup=notes_key)


def register_notes(dp: Dispatcher):
    dp.register_message_handler(show_notes, commands=['show_notes'])
    dp.register_message_handler(create_index, commands=['create_note'])
    dp.register_message_handler(create_title, state=FSMCreate.title)
    dp.register_message_handler(create_body, state=FSMCreate.body)
