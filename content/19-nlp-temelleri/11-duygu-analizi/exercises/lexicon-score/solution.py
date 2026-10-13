import re

GOOD = {"good", "great", "love"}
BAD = {"bad", "awful", "hate"}


def score(text):
    words = re.findall(r"[a-z']+", text.lower())
    return sum((w in GOOD) - (w in BAD) for w in words)

for text in ["I love it", "Bad and awful", "Great, but bad", "No words here"]:
    print(score(text))
