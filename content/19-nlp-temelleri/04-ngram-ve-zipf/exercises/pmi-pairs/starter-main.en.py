import math
import re
from collections import Counter

from text_data import make_reviews

docs = [re.findall(r"[a-z']+", r["text"].lower()) for r in make_reviews(2000)]
unigrams = Counter(w for d in docs for w in d)
bigrams = Counter(b for d in docs for b in zip(d, d[1:]))
n_uni, n_bi = sum(unigrams.values()), sum(bigrams.values())


def top_pmi(min_count, k):
    return []


for pair in top_pmi(50, 4):
    print(pair)
