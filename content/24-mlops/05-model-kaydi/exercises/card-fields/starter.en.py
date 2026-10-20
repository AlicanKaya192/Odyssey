REQUIRED = ["name", "version", "intended_use", "data", "metrics", "limitations"]


def missing_fields(card):
    # Is every field in REQUIRED present and filled in the card?
    pass


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
