import re

SLOT = re.compile(r"\{\{(\w+)\}\}")


def check_values(template, values):
    names = set(SLOT.findall(template))
    return [sorted(names - values.keys()), sorted(values.keys() - names)]


T = "Hi {{name}}, order {{order_id}}: {{message}}"
print(check_values(T, {"name": "Ada", "order": "ORD-1"}))
print(check_values(T, {"name": "A", "order_id": 1, "message": "x"}))
