import re

STEP = re.compile(r"(\d+(?:\.\d+)?) ([-+*/]) (\d+(?:\.\d+)?) = (\d+(?:\.\d+)?)")


def wrong_steps(text):
    return []


print(wrong_steps("2 * 12.50 = 25.00\n40 / 4 = 12"))
print(wrong_steps("10 - 2.5 = 7.5"))
