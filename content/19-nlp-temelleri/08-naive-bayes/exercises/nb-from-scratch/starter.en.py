import math
from collections import Counter

TRAIN = [("great battery great sound", "pos"), ("love the sound", "pos"),
         ("battery died fast", "neg"), ("terrible sound and battery", "neg"),
         ("works great", "pos")]


def train(data):
    priors = Counter(label for _, label in data)
    counts = {label: Counter() for label in priors}
    for text, label in data:
        counts[label].update(text.split())
    vocab = {w for text, _ in data for w in text.split()}
    return priors, counts, vocab


def predict(text, model=train(TRAIN)):
    return "pos"


for text in ["great sound", "battery died", "terrible", "unknown words"]:
    print(text, "->", predict(text))
