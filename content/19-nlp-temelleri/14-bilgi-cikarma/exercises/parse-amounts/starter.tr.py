import re


def parse_amounts(text):
    return []

print(parse_amounts("Paid $1,200.00, refunded $5 and $12.49."))
print(parse_amounts("No money here: 2.49"))
