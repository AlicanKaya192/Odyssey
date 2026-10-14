import json
import re


def parse_json(text):
    return [None, "failed"]


FENCE = "`" * 3
for text in ['{"a": 1}', FENCE + 'json\n{"a": 2}\n' + FENCE,
             'Here: {"a": 3} ok', "{'a': 4}"]:
    print(parse_json(text))
