import re

GOOD = {"good", "great", "love", "worth"}
BAD = {"bad", "awful", "hate"}
NEGATORS = {"not", "never", "can't"}


def negated(text, window):
    total, left = 0, 0
    for word in re.findall(r"[a-z']+|[.,!?]", text.lower()):
        if word in ".,!?":
            left = 0
        elif word in NEGATORS:
            left = window
        else:
            value = (word in GOOD) - (word in BAD)
            total += -value if left else value
            left = max(left - 1, 0)
    return total

print(negated("Not worth it.", 3))
print(negated("It is not bad. It is great.", 3))
print(negated("Not really very good.", 2))
