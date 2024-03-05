import re
from datetime import datetime


def generate_test_number(test_id):  # generate test number from test id and current date
    test_id = str(int(test_id) + 1)
    # date = datetime.now().strftime("%d%m%Y")
    test_number = test_id
    return int(test_number)


async def match_user_answers(user_answers):
    test_answers = re.findall(r'[a-zA-Z]', user_answers)
    test_length = len(test_answers)
    all_answers = {}
    for i in range(len(test_answers)):
        all_answers[i + 1] = test_answers[i]
    return test_length, all_answers


async def calculate_score(test_length, all_answers: str, user_answers: dict):
    # BRUTE FORCE
    correct_answers = ""
    total_score = 0
    for i in range(1, test_length + 1):
        if user_answers[i] == all_answers[i - 1]:
            correct_answers += f"{i}-✅, "
            total_score += 1
        else:
            correct_answers += f"{i}-❌, "
    persentage = round((total_score / test_length) * 100, 2)
    return correct_answers, total_score, persentage
