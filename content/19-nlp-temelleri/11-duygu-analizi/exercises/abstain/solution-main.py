import re

import numpy as np
from text_data import make_reviews

POSITIVE = {"good", "solid", "comfortable", "reliable", "sturdy", "nice",
            "quiet", "great", "excellent", "perfect", "fantastic",
            "impressive", "love", "loves", "worth", "better", "well", "needed"}
NEGATIVE = {"bad", "weak", "flimsy", "poor", "uncomfortable", "loud",
            "fragile", "terrible", "awful", "useless", "disappointing", "hate",
            "worse", "waste", "broke", "damaged", "late", "returned",
            "stopped", "never"}
NEGATORS = {"not", "can't", "never", "no", "don't", "didn't"}


def negated_score(text):
    total, left = 0, 0
    for word in re.findall(r"[a-z']+|[.,!?]", text.lower()):
        if word in ".,!?":
            left = 0
        elif word in NEGATORS:
            left = 3
        else:
            value = (word in POSITIVE) - (word in NEGATIVE)
            total += -value if left else value
            left = max(left - 1, 0)
    return total


reviews = make_reviews(2000)
scores = np.array([negated_score(r["text"]) for r in reviews])
labels = np.array([r["label"] for r in reviews])


def coverage_accuracy(margin):
    keep = np.abs(scores) > margin
    pred = np.where(scores > 0, "positive", "negative")
    accuracy = (pred[keep] == labels[keep]).mean()
    return [round(float(keep.mean()), 3), round(float(accuracy), 3)]


for margin in [0, 1, 2]:
    print(margin, coverage_accuracy(margin))
