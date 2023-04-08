from aiogram.utils import executor
from tg import create_dp

if __name__ == '__main__':
    executor.start_polling(create_dp())
