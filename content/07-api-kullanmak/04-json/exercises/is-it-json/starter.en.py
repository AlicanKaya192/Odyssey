import json

# is_valid(text): True if json.loads can read it, False on JSONDecodeError


samples = [
    '{"city": "Izmir"}',
    "{'city': 'Izmir'}",
    '{"ok": True}',
    '[1, 2,]',
    'null',
]
# For each text: "valid   {...}" or "invalid {...}"
