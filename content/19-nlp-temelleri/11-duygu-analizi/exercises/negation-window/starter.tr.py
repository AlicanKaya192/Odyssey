import re

GOOD = {"good", "great", "love", "worth"}
BAD = {"bad", "awful", "hate"}
NEGATORS = {"not", "never", "can't"}


def negated(text, window):
    return 0

print(negated("Not worth it.", 3))
print(negated("It is not bad. It is great.", 3))
print(negated("Not really very good.", 2))
