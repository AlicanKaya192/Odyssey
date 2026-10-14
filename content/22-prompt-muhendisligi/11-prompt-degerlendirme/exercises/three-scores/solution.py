def scores(replies, gold, labels):
    exact = valid = right = 0
    for reply, truth in zip(replies, gold):
        exact += reply == truth
        label = reply.strip().lower().rstrip(".!")
        if label in labels:
            valid += 1
            right += label == truth
    return [exact, valid, right]


LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
REPLIES = ["shipping", "Returns.", "It is refunds.", "payment"]
GOLD = ["shipping", "returns", "refunds", "refunds"]
print(scores(REPLIES, GOLD, LABELS))
