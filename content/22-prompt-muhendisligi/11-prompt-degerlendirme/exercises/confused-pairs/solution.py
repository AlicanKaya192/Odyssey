from collections import Counter


def top_confusions(gold, parsed, n):
    counts = Counter((g, p) for g, p in zip(gold, parsed) if g != p)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [[g, p, count] for (g, p), count in ordered[:n]]


GOLD = ["refunds", "refunds", "payment", "shipping", "refunds"]
PARSED = ["payment", "payment", "refunds", "shipping", "needs_review"]
for item in top_confusions(GOLD, PARSED, 2):
    print(item)
