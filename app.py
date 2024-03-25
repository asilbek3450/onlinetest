from aiogram import executor

from loader import dp, db_manager
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    db_manager.create_table()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


def on_shutdown():
    db_manager.conn.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
