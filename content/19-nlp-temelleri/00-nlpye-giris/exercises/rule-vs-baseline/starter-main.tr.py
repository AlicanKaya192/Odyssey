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
    return [0.0, 0.0]

print(compare(2000))
