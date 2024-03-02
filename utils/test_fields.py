# id
# teacher
# subject
# test_number
# quantity_questions
# all_answers
# total_score
# status
import re
from datetime import datetime


def generate_test_number(test_id):  # generate test number from test id and current date
    test_id = str(int(test_id)+1)
    date = datetime.now().strftime("%d%m%Y")
    test_number = date + test_id
    return int(test_number)


async def match_user_answers(user_answers):
    test_answers = re.findall(r'[a-zA-Z]', user_answers)
    test_length = len(test_answers)
    all_answers = {}
    for i in range(len(test_answers)):
        all_answers[str(i + 1)] = test_answers[i]
    return test_length, all_answers


async def total_score(test_length):
    return test_length * 10


async def calculate_score(test_length, all_answers, user_answers):
    correct_answers = 0
    for i in range(test_length):
        if all_answers[str(i + 1)] == user_answers[str(i + 1)]:
            correct_answers += 1
    return correct_answers * 10, correct_answers * 100 // test_length
