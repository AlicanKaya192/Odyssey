import json


def total_from_json(text):
    return None


GOOD = ('{"items": [{"price": 189.9, "count": 1}, '
        '{"price": 12.5, "count": 2}], "discount": 0.1}')
print(total_from_json(GOOD))
print(total_from_json('{"items": [{"price": 12.5, "count": "two"}], "discount": 0}'))
print(total_from_json('{"items": [], "discount": 0.9}'))
