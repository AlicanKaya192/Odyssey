import json


def is_valid(text):
    try:
        json.loads(text)
    except json.JSONDecodeError:
        return False
    return True


samples = [
    '{"city": "Izmir"}',
    "{'city': 'Izmir'}",
    '{"ok": True}',
    '[1, 2,]',
    'null',
]
for text in samples:
    if is_valid(text):
        print("valid  ", text)
    else:
        print("invalid", text)
