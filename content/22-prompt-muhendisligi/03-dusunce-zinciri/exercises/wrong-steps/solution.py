import re

STEP = re.compile(r"(\d+(?:\.\d+)?) ([-+*/]) (\d+(?:\.\d+)?) = (\d+(?:\.\d+)?)")


def wrong_steps(text):
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "*": lambda a, b: a * b, "/": lambda a, b: a / b}
    wrong = []
    for a, op, b, c in STEP.findall(text):
        if abs(ops[op](float(a), float(b)) - float(c)) > 0.005:
            wrong.append(f"{a} {op} {b} = {c}")
    return wrong


print(wrong_steps("2 * 12.50 = 25.00\n40 / 4 = 12"))
print(wrong_steps("10 - 2.5 = 7.5"))
