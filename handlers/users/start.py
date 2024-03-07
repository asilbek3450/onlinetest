from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.start import start_kb, menu_kb
from loader import dp, bot, db_manager
from utils.check_start_users import is_user_joined_to_channel
from utils.db_api.database import DatabaseManager


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):

    if await is_user_joined_to_channel(user_id=message.from_user.id):
        if db_manager.get_user_by_user_id(message.from_user.id) is None:
            await message.answer(f"Xush kelibsiz, to'liq ismingizni kiriting!")
            await state.set_state("get_full_name")
        else:
            await message.answer(f"Bo'limlardan birini tanlang.", reply_markup=menu_kb)
    else:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n"
                             f"Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling 👇\n\n", reply_markup=start_kb)


@dp.message_handler(state="get_full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    db_manager.add_user(full_name=full_name, user_id=message.from_user.id)
    await message.answer(f"Tabriklayman! Siz muvaffaqiyatli ro'yxatdan o'tdingiz! Bo'limlardan birini tanlang.",
                         reply_markup=menu_kb)
    await state.finish()


@dp.callback_query_handler(text="check_channel", state="*")
async def check_channel(call: types.CallbackQuery):
    if await is_user_joined_to_channel(call.from_user.id):
        await call.message.edit_text("Tabriklayman! Siz kanalga a'zo bo'libsiz! Bo'limlardan birini tanlang.",
                                     reply_markup=menu_kb)
    else:
        await call.message.edit_text("Iltimos, kanalga a'zo bo'ling!", reply_markup=start_kb)
