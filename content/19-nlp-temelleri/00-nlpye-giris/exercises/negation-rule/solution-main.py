from text_data import make_reviews

GOOD = {"good", "great", "excellent", "perfect",
        "love", "worth", "fantastic", "comfortable"}
BAD = {"bad", "terrible", "awful", "broke",
       "hate", "waste", "poor", "useless"}


def predict_neg(text):
    words = [w.strip(".,!?") for w in text.lower().split()]
    score = 0
    for i, w in enumerate(words):
        sign = 1 if w in GOOD else -1 if w in BAD else 0
        if sign and i > 0 and words[i - 1] == "not":
            sign = -sign
        score += sign
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"

print(predict_neg("Not bad for the price."))
print(predict_neg("Not worth the money."))
print(predict_neg("Not really good, to be honest."))
reviews = make_reviews(2000)
print(sum(predict_neg(r["text"]) == r["label"] for r in reviews))
