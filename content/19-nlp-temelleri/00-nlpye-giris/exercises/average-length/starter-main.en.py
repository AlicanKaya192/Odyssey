from text_data import make_reviews


def average_words(n, label):
    return 0.0

for label in ["positive", "neutral", "negative"]:
    print(label, average_words(1000, label))
