import re

NOT_FOUND = "I could not find this in the sources."
SYSTEM = "Answer only from the numbered sources."


def parse_answer(text):
    return [text, []]


print(parse_answer("Valid for 3 years. [1]"))
print(parse_answer("Open 9:00 [2] and online [3]."))
