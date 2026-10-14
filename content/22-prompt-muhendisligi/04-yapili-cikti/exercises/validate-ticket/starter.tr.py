import re

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]


def validate(data):
    return []


print(validate({"category": "refunds", "urgent": False, "order_id": None}))
print(validate({"category": "delivery", "urgent": "yes"}))
print(validate([1, 2]))
