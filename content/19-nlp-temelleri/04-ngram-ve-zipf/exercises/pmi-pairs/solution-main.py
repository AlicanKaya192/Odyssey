import math
import re
from collections import Counter

from text_data import make_reviews

docs = [re.findall(r"[a-z']+", r["text"].lower()) for r in make_reviews(2000)]
unigrams = Counter(w for d in docs for w in d)
bigrams = Counter(b for d in docs for b in zip(d, d[1:]))
n_uni, n_bi = sum(unigrams.values()), sum(bigrams.values())


def pmi(pair):
    together = bigrams[pair] / n_bi
    apart = (unigrams[pair[0]] / n_uni) * (unigrams[pair[1]] / n_uni)
    return math.log2(together / apart)


def top_pmi(min_count, k):
    frequent = [b for b, c in bigrams.items() if c >= min_count]
    return [a + " " + b for a, b in sorted(frequent, key=pmi, reverse=True)[:k]]


for pair in top_pmi(50, 4):
    print(pair)
