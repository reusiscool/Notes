from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from tg.calls import get_user, get_notes, create, del_note
from tg.states import FSMCreate
from tg.keyboards import start_key, notes_key, cancel_key


async def show_notes(message: types.Message):
    tg_id = message.from_user.id
    user_data = get_user(tg_id)
    if user_data['status'] == 'failed':
        await message.answer('You are not logged in', reply_markup=start_key)
        return
    notes_data = get_notes(user_data['id'])
    for note in notes_data:
        await message.answer(f'{note["title"]}\n{note["created"]}\n{note["body"]}',
                             reply_markup=InlineKeyboardMarkup().
                             add(InlineKeyboardButton(text='delete', callback_data=f'delete {note["id"]}')))


async def create_index(message: types.Message):
    tg_id = message.from_user.id
    user_data = get_user(tg_id)
    if user_data['status'] == 'failed':
        await message.answer('You are not logged in', reply_markup=start_key)
        return
    await FSMCreate.title.set()
    await message.answer('Title ->', reply_markup=cancel_key)


async def create_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await FSMCreate.next()
    await message.answer('Body ->', reply_markup=cancel_key)


async def create_body(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    body = message.text
    async with state.proxy() as data:
        title = data['title']
    await state.finish()
    user_data = get_user(tg_id)
    post_data = create(title, body, user_data['id'])
    if post_data['status'] == 'failed':
        await message.answer(post_data['error'], reply_markup=notes_key)
    else:
        await message.answer('Cool', reply_markup=notes_key)


async def delete_note(callback: types.CallbackQuery):
    data = callback.data
    message = callback.message
    try:
        id_ = int(data.split()[1])
    except (IndexError, ValueError):
        await message.answer('Wrong index')
        return
    user_data = get_user(message.from_user.id)
    if user_data['status'] == 'failed':
        await message.answer(user_data['error'])
        return
    data = del_note(user_data['id'], id_)
    if data['status'] == 'failed':
        await message.answer(data['error'])
        return
    await message.answer('Deleted')
    await callback.answer('')


def register_notes(dp: Dispatcher):
    dp.register_message_handler(show_notes, commands=['show_notes'])
    dp.register_message_handler(create_index, commands=['create_note'])
    dp.register_message_handler(create_title, state=FSMCreate.title)
    dp.register_callback_query_handler(delete_note)
    dp.register_message_handler(create_body, state=FSMCreate.body)
