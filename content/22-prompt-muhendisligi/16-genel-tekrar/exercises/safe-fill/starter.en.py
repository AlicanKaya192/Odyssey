import re


def fill(template, values):
    return [template, []]


TEMPLATE = "Hello {name}, order {order} is {status}."
print(fill(TEMPLATE, {"name": "Ada", "order": "ORD-48213",
                      "status": "shipped"})[0])
print(fill(TEMPLATE, {"name": "Ada"}))
