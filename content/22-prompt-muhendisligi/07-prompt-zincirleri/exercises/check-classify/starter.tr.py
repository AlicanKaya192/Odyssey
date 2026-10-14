import json


def check_classify(text, labels):
    return None


LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
for text in ['{"category": "refunds"}', "refunds", '{"category": "late"}', "[1]"]:
    print(check_classify(text, LABELS))
