from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.start import create_test_kb, check_test_kb, menu_kb, active_test_kb
from loader import dp, bot
from utils.regex_test import regex_create_test, regex_check_test
from utils.test_fields import generate_test_number, match_user_answers, calculate_score
from loader import db_manager


@dp.callback_query_handler(text="create_test_with_score", state="*")
async def create_test_with_score(call: types.CallbackQuery):
    text = """
👇👇👇 Yo'riqnoma✅

👇Ballik test yaratish uchun:

test+Ism familiya*Fan nomi*to'g'ri javoblar*ball

ko`rinishida yuboring‼️

👇Misol  uchun:

test+Aliyev Ali*Matematika*abbc...*1.3;2.2;2.2;1.3;...
yoki
test+Aliyev Ali*Matematika*1a2d3c4a...*1.3;2.2;2.2;1.3;...

❗️❗️ ball - har bir testga ball qo'shish uchun ishlatiladi buni to'ldirish quyidagicha:
✅1.3;2.2;2.2;... ko'rinishida ballarni yuboring.

✅o'nli kasrni . bilan bering, orasi ; bilan bering, oxiriga ; qo'ymang

✅Barcha test uchun ball kiriting.

❗️Agar testga ball qo'shishni xoxlamsangiz ball qismiga shunchaki # belgisini qo'shish kifoya (bu xolatda har bir test 1 balldan hisoblanadi)
"""
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
