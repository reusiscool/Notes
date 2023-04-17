import asyncio

from tg.init import create_bot
from tg.calls import get_notifications, get_tg_id


async def notify():
    bot = create_bot()
    for note in get_notifications():
        ids = get_tg_id(note['author_id'])
        for tg_id in ids:
            await bot.send_message(tg_id, f"{note['title']}\n{note['body']}")


async def scheduler():
    while True:
        await notify()
        await asyncio.sleep(10)


async def on_startup(_):
    asyncio.create_task(scheduler())
