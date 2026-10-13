import re

from text_data import make_tickets

tickets = make_tickets(2000)


def order_share(category):
    texts = [t["text"] for t in tickets if t["category"] == category]
    found = [bool(re.search(r"\bORD-\d{5}\b", text)) for text in texts]
    return round(sum(found) / len(found), 3)


for category in ["account", "billing", "refund", "shipping", "technical"]:
    print(category, order_share(category))
