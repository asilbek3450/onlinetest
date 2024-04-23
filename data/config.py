from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
DOMAIN = env.str("DOMAIN")

CHANNEL_URL = env.str("CHANNEL_URL")
CHANNEL_ID = env.str("CHANNEL_ID")
CHANNEL = [
    {'name': "Channel 🌐", "url": CHANNEL_URL, "id": CHANNEL_ID},
]

WEBAPP_HOST = env.str("WEBAPP_HOST")
