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


def aspect_labels(text, aspects):
    totals = {}
    for sentence in re.findall(r"[^.!?]+", text.lower()):
        for aspect in aspects:
            if aspect in sentence:
                totals[aspect] = totals.get(aspect, 0) + negated(sentence, 3)
    return {a: "positive" if s > 0 else "negative" if s < 0 else "neutral"
            for a, s in totals.items()}

text = "The strap is great. The screen is not good. Fast delivery."
print(aspect_labels(text, ["strap", "screen", "battery"]))
