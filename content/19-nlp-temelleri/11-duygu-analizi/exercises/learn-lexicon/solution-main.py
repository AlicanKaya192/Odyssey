import math
import re
from collections import Counter

from text_data import make_reviews

counts = {"positive": Counter(), "negative": Counter()}
for r in make_reviews(1000):
    if r["label"] in counts:
        counts[r["label"]].update(set(re.findall(r"[a-z']+", r["text"].lower())))
sizes = {"positive": 0, "negative": 0}
for r in make_reviews(1000):
    if r["label"] in sizes:
        sizes[r["label"]] += 1
common = counts["positive"] + counts["negative"]


def log_odds(word):
    pos = (counts["positive"][word] + 1) / (sizes["positive"] + 2)
    neg = (counts["negative"][word] + 1) / (sizes["negative"] + 2)
    return math.log(pos / neg)


def top_words(label, k):
    words = sorted(sorted(w for w in common if common[w] >= 5), key=log_odds)
    if label == "positive":
        words = words[::-1]
    return words[:k]


print(top_words("negative", 4))
print(top_words("positive", 4))
