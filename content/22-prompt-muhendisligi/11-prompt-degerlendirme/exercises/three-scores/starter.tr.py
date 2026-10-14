def scores(replies, gold, labels):
    return [0, 0, 0]


LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
REPLIES = ["shipping", "Returns.", "It is refunds.", "payment"]
GOLD = ["shipping", "returns", "refunds", "refunds"]
print(scores(REPLIES, GOLD, LABELS))
