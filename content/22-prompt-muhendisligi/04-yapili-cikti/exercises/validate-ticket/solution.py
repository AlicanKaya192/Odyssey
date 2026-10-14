import re

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]


def validate(data):
    if not isinstance(data, dict):
        return ["object"]
    errors = ["missing:" + key for key in ["category", "urgent", "order_id"]
              if key not in data]
    if "category" in data and data["category"] not in LABELS:
        errors.append("category")
    if "urgent" in data and not isinstance(data["urgent"], bool):
        errors.append("urgent")
    order = data.get("order_id")
    if order is not None and not re.fullmatch(r"ORD-\d{5}", str(order)):
        errors.append("order_id")
    return errors


print(validate({"category": "refunds", "urgent": False, "order_id": None}))
print(validate({"category": "delivery", "urgent": "yes"}))
print(validate([1, 2]))
