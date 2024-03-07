from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.start import create_test_kb, check_test_kb, menu_kb, active_test_kb
from loader import dp, db_manager
from utils.regex_test import regex_create_test, regex_check_test
from utils.test_fields import generate_test_number, match_user_answers, calculate_score


@dp.callback_query_handler(text="check_test")
async def check_test(call: types.CallbackQuery):
    documentation = """👇👇👇 Yo'riqnoma✅

👇Test javoblarini yuborish uchun ‼️

test kodi*Ism familiya*abbccdd...*
yoki
test kodi*Ism familiya*1a2d3c4a5b...*

kabi ko`rinishlarda yuboring✅

👇Misol:

1234*Aliyev Ali*abbccdd...
yoki
1234*Aliyev Ali*1a2d3c4a5b...

Testni yuborish uchun faqat bir marta imkoniyat beriladi!🔒"""
    await call.message.edit_text(documentation, reply_markup=check_test_kb)


@dp.message_handler(regexp="(\d+)\*([A-Za-z]+ [A-Za-z]+)\*([\w]+)")
async def check_test(message: types.Message):
    test_number, full_name, test_answers = await regex_check_test(message.text)
    test_length, all_user_answers = await match_user_answers(test_answers)

    test = db_manager.get_test_by_test_number(test_number)
    quantity_questions = test[4]

    if test[7] == 0:
        await message.answer(f"Test yakunlangan!")
        return
    if db_manager.is_user_test_connection_exists(user_id=message.from_user.id, test_id=test[0]):
        await message.answer(f"Testni bir marta topshirgansiz!")
        return
    if test_length != quantity_questions:
        await message.answer(f"Testlar soni mos kelmadi!")
        return

    correct_answers, total_score, persentage = await calculate_score(quantity_questions, test[5], all_user_answers)
    user = db_manager.get_user_by_full_name(full_name)
    try:
        db_manager.add_user_test_connection(user[0], test[0], test_answers, correct_answers, total_score, persentage)

        text_message = f"👤 Foydalanuvchi:\n" \
                       f"    {full_name}\n\n" \
                       f"    📚 Fan: {test[2]}\n" \
                       f"    📖 Test kodi: {test[3]}\n" \
                       f"    ✏️ Jami savollar soni: {quantity_questions} ta\n" \
                       f"    ✅ To'g'ri javoblar soni: {total_score}\n" \
                       f"    📊 To'plangan ball: {total_score} ball\n" \
                       f"    🔣 Foiz : {persentage} %\n" \
                       f"    --------------------------------\n" \
                       f"    🕐 Sana, vaqt: {message.date}"

        await message.answer(text_message, reply_markup=ReplyKeyboardRemove())

    except:
        await message.answer("Siz bu testni topshirgansiz. Qayta jo'natish mumkin emas!", reply_markup=ReplyKeyboardRemove())


