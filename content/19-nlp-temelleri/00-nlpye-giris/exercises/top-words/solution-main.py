from collections import Counter
from text_data import make_reviews


def top_words(n, label, k):
    words = Counter()
    for r in make_reviews(n):
        if r["label"] == label:
            for w in r["text"].lower().split():
                words[w.strip(".,!?")] += 1
    return words.most_common(k)

for word, count in top_words(1000, "negative", 5):
    print(word, count)
