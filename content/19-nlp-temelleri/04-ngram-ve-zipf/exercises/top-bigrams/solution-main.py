import re
from collections import Counter

from text_data import make_reviews

reviews = make_reviews(2000)
docs = [re.findall(r"[a-z']+", r["text"].lower()) for r in reviews]


def top_bigrams(label, k):
    pairs = Counter()
    for d, r in zip(docs, reviews):
        if r["label"] == label:
            pairs.update(zip(d, d[1:]))
    return [a + " " + b for (a, b), _ in pairs.most_common(k)]


for label in ["neutral", "negative"]:
    print(label)
    for pair in top_bigrams(label, 3):
        print("  ", pair)
