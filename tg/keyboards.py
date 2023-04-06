from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Register')
b2 = KeyboardButton('/Login')

start_key = ReplyKeyboardMarkup(resize_keyboard=True)
start_key.row(b1, b2)


b1 = KeyboardButton('/show_notes')
b2 = KeyboardButton('/show_deleted_notes')
b3 = KeyboardButton('/logout')
notes_key = ReplyKeyboardMarkup(resize_keyboard=True)
notes_key.row(b1, b2, b3)
