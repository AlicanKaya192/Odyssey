LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]


def parse_label(text, labels):
    return "needs_review"


for text in ["Refunds.", " payment\n", "Returns?", "It is shipping."]:
    print(repr(text), parse_label(text, LABELS))
