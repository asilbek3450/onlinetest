from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.start import menu_kb
from loader import dp


@dp.callback_query_handler(text="back_to_menu", state="*")
async def back_to_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Bo'limlardan birini tanlang.", reply_markup=menu_kb)
    await state.finish()
