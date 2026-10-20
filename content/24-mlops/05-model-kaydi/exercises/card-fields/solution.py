REQUIRED = ["name", "version", "intended_use", "data", "metrics", "limitations"]


def missing_fields(card):
    missing = []
    for field in REQUIRED:
        if field not in card or card[field] in ("", None, {}, []):
            missing.append(field)
    return missing


card = {
    "name": "churn",
    "version": 3,
    "intended_use": "choose customers to call",
    "data": "",
    "metrics": {"accuracy": 0.818},
}
print(missing_fields(card))
card["data"] = "5000 customers, month 0"
card["limitations"] = "this service only"
print(missing_fields(card))
