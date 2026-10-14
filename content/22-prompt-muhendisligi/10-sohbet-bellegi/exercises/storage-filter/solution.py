import re

SECRET = re.compile(r"password|passcode|\b\d{4} \d{4} \d{4} \d{4}\b", re.I)
ORDER = re.compile(r"\bORD-\d{5}\b")


def store_all(texts):
    statuses, orders = [], []
    for text in texts:
        if SECRET.search(text):
            statuses.append("not stored")
            continue
        statuses.append("stored")
        orders += ORDER.findall(text)
    return [statuses, orders]


TEXTS = ["Order ORD-48213 please.",
         "My Password is secret1 for ORD-10077.",
         "Card 1234 5678 9012 3456",
         "Also ORD-23345 and ORD-55102."]
statuses, orders = store_all(TEXTS)
for status in statuses:
    print(status)
print(orders)
