from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.start import create_test_kb, check_test_kb, menu_kb, active_test_kb
from loader import dp
from utils.regex_test import regex_create_test, regex_check_test
from utils.test_fields import generate_test_number, match_user_answers, calculate_score
from utils.db_api.database import DatabaseManager


class TestCreationStates(StatesGroup):
    active_test_number = State()
    is_test_active = State()


@dp.callback_query_handler(text="create_test")
async def create_test(call: types.CallbackQuery):
    documentation = """👇👇👇 Yo'riqnoma✅

👇Test yaratish uchun:

test*Ism familiya*Fan nomi*to'g'ri javoblar

ko`rinishida yuboring‼️

👇Misol:

test*Aliyev Ali*Matematika*abbccdd...*#
yoki
test*Aliyev Ali*Matematika*1a2d3c4a5b...*#
"""
    await call.message.edit_text(documentation, reply_markup=create_test_kb)
    await TestCreationStates.active_test_number.set()


@dp.message_handler(regexp=r"test\*([A-Za-z]+ [A-Za-z]+)\*([A-Za-z]+[0-9]*)\*([A-Za-z\d]+)\*#",
                    state=TestCreationStates.active_test_number)
async def create_test(message: types.Message, state: FSMContext):
    full_name, subject, user_answers = await regex_create_test(message.text)
    quantity_questions, all_answers = await match_user_answers(user_answers)
    total_score = quantity_questions * 10

    db = DatabaseManager("online_test.db")

    test_number = generate_test_number(db.get_current_test_id())
    db.add_test(full_name, subject, test_number, quantity_questions, user_answers, total_score, status=True)
    new_test = db.get_test_by_test_number(test_number)
    await state.update_data(active_test_number=new_test[3])
    await TestCreationStates.next()

    db.close()
    text_message = f"Test yaratildi!\n\n" \
                   f"👤 O'qituvchi: {new_test[1]}\n" \
                   f"📚 Fan: {new_test[2]}\n\n" \
                   f"📕 Test raqami: {new_test[3]}\n" \
                   f"🔢 Testlar soni: {new_test[4]}\n" \
                   f"📝 Test javoblari: {new_test[5]}\n" \
                   f"📊 Maksimal ball: {new_test[6]}\n"

    await message.answer(text_message, reply_markup=active_test_kb)


@dp.callback_query_handler(text="finish_test", state=TestCreationStates.is_test_active)
async def finish_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Test yakunlandi!", reply_markup=menu_kb)
    state_data = await state.get_data()
    db = DatabaseManager("online_test.db")
    test = db.get_test_by_test_number(state_data["active_test_number"])
    db.update_test_status(test[3], status=False)
    db.close()
    await state.finish()


@dp.callback_query_handler(text="current_users", state="*")
async def current_users(call: types.CallbackQuery, state: FSMContext):
    db = DatabaseManager("online_test.db")
    state_data = await state.get_data()
    try:
        users = db.get_user_test_connection_by_test_id(state_data["active_test_number"])
    except TypeError:
        users = None

    if users:
        text_message = "Testdagi foydalanuvchilar:\n\n"
        cnt = 1
        for i in users:
            user_full_name = db.get_user_by_id(i[1])[1]
            text_message += f"{cnt}) {user_full_name} - {i[5]} ball\n"
            cnt += 1
    else:
        text_message = "Testda foydalanuvchilar yo'q!"
    await call.message.answer(text_message)

    db.close()
