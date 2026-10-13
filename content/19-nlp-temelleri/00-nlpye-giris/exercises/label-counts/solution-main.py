from collections import Counter
from text_data import make_reviews


def label_counts(n):
    reviews = make_reviews(n)
    return dict(Counter(r["label"] for r in reviews))

for label, count in label_counts(500).items():
    print(label, count)
