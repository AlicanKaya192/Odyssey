def decide(score, threshold, customer):
    if score is None:
        offer = customer["support_calls"] >= 2
    else:
        offer = score >= threshold
    return "offer" if offer else "no offer"


customer = {"support_calls": 3}
print(decide(0.42, 0.31, customer))
print(decide(0.12, 0.31, customer))
print(decide(None, 0.31, customer))
print(decide(None, 0.31, {"support_calls": 1}))
