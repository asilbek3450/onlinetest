from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNEL_ID
from keyboards.inline.start import start_kb, menu_kb
from loader import dp, bot
from utils.check_start_users import is_user_joined_to_channel


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id):
        await message.answer(f"Bo'limlardan birini tanlang.", reply_markup=menu_kb)
    else:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n"
                             f"Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling 👇\n\n", reply_markup=start_kb)


@dp.callback_query_handler(text="check_channel")
async def check_channel(call: types.CallbackQuery):
    if await is_user_joined_to_channel(call.from_user.id):
        await call.message.edit_text("Tabriklayman! Siz kanalga a'zo bo'libsiz! Bo'limlardan birini tanlang.", reply_markup=menu_kb)
    else:
        await call.message.edit_text("Iltimos, kanalga a'zo bo'ling!", reply_markup=start_kb)


