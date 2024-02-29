import re

from aiogram import types

from keyboards.inline.start import create_test_kb, check_test_kb, menu_kb
from loader import dp
from utils.regex_test import regex_create_test, regex_check_test


@dp.callback_query_handler(text="create_test")
async def create_test(call: types.CallbackQuery):
    documentation = """👇👇👇 Yo'riqnoma✅

👇Test yaratish uchun:

test+Ism familiya*Fan nomi*to'g'ri javoblar

ko`rinishida yuboring‼️

👇Misol:

test*Aliyev Ali*Matematika*abbccdd...#
yoki
test*Aliyev Ali*Matematika*1a2d3c4a5b...#
"""
    await call.message.edit_text(documentation, reply_markup=create_test_kb)


@dp.callback_query_handler(text="check_test")
async def check_test(call: types.CallbackQuery):
    documentation = """👇👇👇 Yo'riqnoma✅

👇Test javoblarini yuborish uchun ‼️

test kodi*Ism familiya*abbccdd...*
yoki
test kodi*Ism familiya*1a2d3c4a5b...*

kabi ko`rinishlarda yuboring✅

👇Misol:

1234*Aliyev Ali*abbccdd...*
yoki
1234*Aliyev Ali*1a2d3c4a5b...*"""
    await call.message.edit_text(documentation, reply_markup=check_test_kb)


@dp.callback_query_handler(text="back_to_menu")
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text("Bo'limlardan birini tanlang.", reply_markup=menu_kb)


@dp.message_handler(regexp="test\*([A-Za-z]+ [A-Za-z]+)\*([A-Za-z]+)\*([A-Za-z\d]+)\*#")
async def create_test(message: types.Message):
    full_name, subject, test_answers = await regex_create_test(message.text)
    test_number = 1234  # This is a test number, you can generate it as you want
    await message.answer(f"Test yaratildi!\n"
                         f"🔢: {test_number}\n"
                         f"👤: {full_name}\n"
                         f"📚: {subject}\n"
                         f"📝: {test_answers}")


@dp.message_handler(regexp="(\d+)\*([A-Za-z]+ [A-Za-z]+)\*([\w]+)")
async def check_test(message: types.Message):
    test_number, full_name, test_answers = await regex_check_test(message.text)
    await message.answer(f"Test tekshirildi!\n"
                         f"🔢: {test_number}\n"
                         f"👤: {full_name}\n"
                         f"📝: {test_answers}")
