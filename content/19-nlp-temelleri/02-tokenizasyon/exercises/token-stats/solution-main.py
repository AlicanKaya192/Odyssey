import re

from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews


def token_stats(n):
    texts = [r["text"].lower() for r in make_reviews(n)]
    analyze = CountVectorizer().build_analyzer()
    results = []
    for tokenize in [str.split, lambda t: re.findall(r"\w+|[^\w\s]", t), analyze]:
        tokens = [tok for t in texts for tok in tokenize(t)]
        results.append([len(tokens), len(set(tokens))])
    return results


for name, (total, distinct) in zip(["split", "regex", "sklearn"], token_stats(2000)):
    print(name, total, distinct)
