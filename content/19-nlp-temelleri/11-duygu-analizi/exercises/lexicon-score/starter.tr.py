import re

GOOD = {"good", "great", "love"}
BAD = {"bad", "awful", "hate"}


def score(text):
    return 0

for text in ["I love it", "Bad and awful", "Great, but bad", "No words here"]:
    print(score(text))
