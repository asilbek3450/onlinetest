import asyncio
import json

import aiohttp

from data import config

DOMAIN = config.DOMAIN
url = {
    "url": "https://" + DOMAIN + "/api/telegram",
}
API_URL = "https://api.telegram.org/bot%s/setWebhook" % config.BOT_TOKEN


async def register_webhook():
    headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=json.dumps(url), headers=headers) as resp:
            try:
                assert resp.status == 200
                print("Webhook registered")
            except Exception as e:
                return {'success': False, 'message': str(e)}
            result = await resp.json()
            return {'success': result['result'], 'message': result['description']}


if __name__ == '__main__':
    response = asyncio.run(register_webhook())
    print(response['message'])
    if response['success']:
        exit(0)
    else:
        exit(1)
