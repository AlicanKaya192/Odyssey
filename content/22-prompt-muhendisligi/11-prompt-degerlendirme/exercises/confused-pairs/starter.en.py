from collections import Counter


def top_confusions(gold, parsed, n):
    return []


GOLD = ["refunds", "refunds", "payment", "shipping", "refunds"]
PARSED = ["payment", "payment", "refunds", "shipping", "needs_review"]
for item in top_confusions(GOLD, PARSED, 2):
    print(item)
