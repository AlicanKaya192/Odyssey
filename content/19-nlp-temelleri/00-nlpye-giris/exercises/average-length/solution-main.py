from text_data import make_reviews


def average_words(n, label):
    lengths = [len(r["text"].split()) for r in make_reviews(n) if r["label"] == label]
    return round(sum(lengths) / len(lengths), 1)

for label in ["positive", "neutral", "negative"]:
    print(label, average_words(1000, label))
