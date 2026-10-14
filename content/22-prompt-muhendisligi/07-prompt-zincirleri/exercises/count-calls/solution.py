def count_calls(labels, needs_order):
    fixed = 3 * len(labels)
    conditional = sum(3 if label in needs_order else 2 for label in labels)
    return [fixed, conditional]


print(count_calls(["shipping", "payment", "warranty"],
                  ["shipping", "returns", "refunds"]))
