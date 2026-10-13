import re


def find_orders(text):
    return re.findall(r"\bORD-\d{5}\b", text)

print(find_orders("Order ORD-27246 and ORD-12345 are late."))
print(find_orders("Wrong: ORD-123456, ord-12345, ORD-1234."))
