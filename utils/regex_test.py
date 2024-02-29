import re


async def regex_create_test(test_string):
    pattern = r"test\*([A-Za-z]+ [A-Za-z]+)\*([A-Za-z]+)\*([A-Za-z\d]+)\*#"  # test*Aliyev Ali*Matematika*abbccdd...*#
    match = re.match(pattern, test_string)
    if match:
        full_name = match.group(1)
        subject = match.group(2)
        test_answers = match.group(3)
        return full_name, subject, test_answers
    else:
        return f"Testni yaratishda xatolik bor! {test_string}"


async def regex_check_test(input_text):
    pattern = r"(\d+)\*([A-Za-z]+ [A-Za-z]+)\*([\w]+)"  # 1234*Aliyev Ali*abbccdd...
    match = re.match(pattern, input_text)
    if match:
        test_number = match.group(0)
        full_name = match.group(1)
        test_answers = match.group(2)
        return test_number, full_name, test_answers
    else:
        return f"Testni tekshirishda xatolik bor! {input_text}"
    