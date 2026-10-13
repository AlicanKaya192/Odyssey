from text_data import make_reviews

GOOD = {"good", "great", "excellent", "perfect",
        "love", "worth", "fantastic", "comfortable"}
BAD = {"bad", "terrible", "awful", "broke",
       "hate", "waste", "poor", "useless"}


def predict_neg(text):
    words = [w.strip(".,!?") for w in text.lower().split()]
    score = sum(w in GOOD for w in words) - sum(w in BAD for w in words)
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
