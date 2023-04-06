from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMRegister(StatesGroup):
    name = State()
    password = State()


class FSMLogin(StatesGroup):
    name = State()
    password = State()
