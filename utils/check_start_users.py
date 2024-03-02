from data.config import CHANNEL_ID, CHANNEL_URL
from loader import bot


async def is_user_joined_to_channel(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # print("Member status:", member.status)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking user membership: {e}")
        return False
