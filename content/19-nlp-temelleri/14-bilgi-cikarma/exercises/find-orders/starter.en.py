import re


def find_orders(text):
    return []

print(find_orders("Order ORD-27246 and ORD-12345 are late."))
print(find_orders("Wrong: ORD-123456, ord-12345, ORD-1234."))
