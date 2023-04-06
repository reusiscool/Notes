from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Register')
b2 = KeyboardButton('/Login')

start_key = ReplyKeyboardMarkup(resize_keyboard=True)
start_key.row(b1, b2)
