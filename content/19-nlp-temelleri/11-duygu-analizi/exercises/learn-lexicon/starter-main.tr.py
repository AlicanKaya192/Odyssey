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
    return 0.0


def top_words(label, k):
    return []


print(top_words("negative", 4))
print(top_words("positive", 4))
