import json
from collections import Counter


def count_levels(lines):
    counts = Counter(json.loads(line)["level"] for line in lines)
    return [f"{level}: {n}" for level, n in sorted(counts.items())]

LINES = [
    '{"level": "INFO", "event": "login"}',
    '{"level": "WARNING", "event": "login"}',
    'this is not json',
    '{"level": "WARNING", "event": "login"}',
    '{"level": "ERROR", "event": "db"}',
]
for line in count_levels(LINES):
    print(line)
