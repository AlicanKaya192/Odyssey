import json


def total_from_json(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    items, discount = data.get("items"), data.get("discount")
    if not isinstance(items, list) or not items:
        return None
    if not isinstance(discount, (int, float)) or not 0 <= discount <= 0.5:
        return None
    subtotal = 0
    for item in items:
        price, count = item.get("price"), item.get("count")
        if not isinstance(price, (int, float)) or price <= 0:
            return None
        if not isinstance(count, int) or count < 1:
            return None
        subtotal += price * count
    return round(subtotal * (1 - discount), 2)


GOOD = ('{"items": [{"price": 189.9, "count": 1}, '
        '{"price": 12.5, "count": 2}], "discount": 0.1}')
print(total_from_json(GOOD))
print(total_from_json('{"items": [{"price": 12.5, "count": "two"}], "discount": 0}'))
print(total_from_json('{"items": [], "discount": 0.9}'))
