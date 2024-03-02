from aiogram import types

from data.config import CHANNEL_URL

start_kb = types.InlineKeyboardMarkup(row_width=1)
start_kb.add(types.InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url=CHANNEL_URL))
start_kb.add(types.InlineKeyboardButton(text="🔄 Tekshirish", callback_data="check_channel"))

menu_kb = types.InlineKeyboardMarkup(row_width=1)
menu_kb.add(types.InlineKeyboardButton(text="➕ Test yaratish", callback_data="create_test"))
menu_kb.add(types.InlineKeyboardButton(text="📝 Testni tekshirish", callback_data="check_test"))

back_to_menu = types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")

create_test_kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        types.InlineKeyboardButton(text="✅ Ballik test", callback_data="create_test_with_score"),
        back_to_menu
    ]
])

active_test_kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        types.InlineKeyboardButton(text="Joriy holat", callback_data="current_users"),
        types.InlineKeyboardButton(text="Yakunlash", callback_data="finish_test")
    ]
])

check_test_kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        types.InlineKeyboardButton(text="✅ Ballik test", callback_data="check_test_with_score"),
        back_to_menu
    ]
])

