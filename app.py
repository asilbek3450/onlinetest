from aiogram import types

from aiogram import executor
from aiohttp import web

from data import config
from loader import dp, db_manager
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

app = web.Application()

webhook_path = f"/{config.BOT_TOKEN}/"


async def set_webhook():
    webhook_url = f"{config.WEBAPP_HOST}{webhook_path}"
    await dp.bot.set_webhook(webhook_url)


async def on_startup(dispatcher):
    db_manager.create_table()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await set_webhook()


def on_shutdown():
    db_manager.conn.close()


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]
    if token == config.BOT_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)

        await dp.process_updates(update)
        return web.Response()
    return web.Response(status=403)

app.router.add_post(f'/{config.BOT_TOKEN}/', handle_webhook)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    web.run_app(
        app,
        host='0.0.0.0',
        port=8080,

    )
