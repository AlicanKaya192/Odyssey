from collections import Counter
from text_data import make_reviews

GOOD = {"good", "great", "excellent", "perfect",
        "love", "worth", "fantastic", "comfortable"}
BAD = {"bad", "terrible", "awful", "broke",
       "hate", "waste", "poor", "useless"}


def predict(text):
    words = [w.strip(".,!?") for w in text.lower().split()]
    score = sum(w in GOOD for w in words) - sum(w in BAD for w in words)
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def compare(n):
    reviews = make_reviews(n)
    rule = sum(predict(r["text"]) == r["label"] for r in reviews) / n
    top_count = Counter(r["label"] for r in reviews).most_common(1)[0][1]
    return [round(rule, 3), round(top_count / n, 3)]

print(compare(2000))
