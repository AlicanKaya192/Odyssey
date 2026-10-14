import json


def check_classify(text, labels):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict) and data.get("category") in labels:
        return data["category"]
    return None


LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
for text in ['{"category": "refunds"}', "refunds", '{"category": "late"}', "[1]"]:
    print(check_classify(text, LABELS))
