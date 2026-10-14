LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]


def parse_label(text, labels):
    label = text.strip().lower().rstrip(".!")
    return label if label in labels else "needs_review"


for text in ["Refunds.", " payment\n", "Returns?", "It is shipping."]:
    print(repr(text), parse_label(text, LABELS))
