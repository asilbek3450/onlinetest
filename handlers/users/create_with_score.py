from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from handlers.users.create_test import TestCreationStates
from keyboards.inline.start import create_test_kb, check_test_kb, menu_kb, active_test_kb
from loader import dp, bot
from utils.regex_test import regex_create_test_with_score
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
    await TestCreationStates.active_test_number.set()


# test creation: regexp=r"test\*([A-Za-z]+ [A-Za-z]+)\*([A-Za-z]+[0-9]*)\*([A-Za-z\d]+)\*#" - for example: test*Aliyev Ali*Matematika*abbccdd...* or test*Aliyev Ali*Matematika*1a2d3c4a5b...*
# test creation with score: regexp=r"test\+([A-Za-z]+ [A-Za-z]+)\*([A-Za-z]+[0-9]*)\*([A-Za-z\d]+)\*([0-9.]+)\*#" - for example: test+Aliyev Ali*Matematika*abbc...*1.3;2.2;2.2;1.3;... or test+Aliyev Ali*Matematika*1a2d3c4a...*1.3;2.2;2.2;1.3;...

@dp.message_handler(regexp=r"test\+([A-Za-z]+ [A-Za-z]+)\*([A-Za-z]+[0-9]*)\*([A-Za-z\d]+)\*([0-9.]+)\*#", state="*")
async def create_test_with_score(message: types.Message, state: FSMContext):
    full_name, subject, user_answers, score = await regex_create_test_with_score(message.text)
    quantity_questions, all_answers = await match_user_answers(user_answers)
    total_score = sum([float(i) for i in score.split(";")])
    all_answers_str = ""
    for i in all_answers:
        all_answers_str += f"{all_answers[i]}"

    test_number = generate_test_number(db_manager.get_current_test_id())
    db_manager.add_test(full_name, subject, test_number, quantity_questions, all_answers_str, total_score, status=True)
    new_test = db_manager.get_test_by_test_number(test_number)
    await state.update_data(active_test_number=new_test[3])
    await TestCreationStates.next()

    documentation = (f"Testda qatnashuvchilar quyidagi ko'rinishda javob yuborishlari mumkin:\n\n"
                     f"{new_test[3]}*Ism Familiya*abcde... ({new_test[4]}ta)\n"
                     f"Yoki\n"
                     f"{new_test[3]}*Ism Familiya*1a2d3c4a5b... ({new_test[4]}ta)")

    text_message = f"Test yaratildi!\n\n" \
                   f"👤 O'qituvchi: {new_test[1]}\n" \
                   f"📚 Fan: {new_test[2]}\n\n" \
                   f"🔢 Test raqami: {new_test[3]}\n" \
                   f"📝 Testlar soni: {new_test[4]}\n" \
                   f"🔢 Test balli: {new_test[6]}\n\n" \
                   f"📌 Test javoblari:\n{new_test[5]}\n\n" \
                   f"📝 Test javoblarini yuborish uchun:\n\n" \
                   f"{documentation}"

    await message.answer(text=text_message, reply_markup=active_test_kb)
    await state.finish()

#
# @dp.callback_query_handler(text="finish_test", state=TestCreationStates.is_test_active)
# async def finish_test(call: types.CallbackQuery, state: FSMContext):
