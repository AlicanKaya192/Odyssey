import json

# is_valid(text): json.loads okuyabiliyorsa True, JSONDecodeError verirse False


samples = [
    '{"city": "Izmir"}',
    "{'city': 'Izmir'}",
    '{"ok": True}',
    '[1, 2,]',
    'null',
]
# Her metin icin: "valid   {...}" ya da "invalid {...}"
