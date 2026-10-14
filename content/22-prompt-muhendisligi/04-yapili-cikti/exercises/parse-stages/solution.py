import json
import re


def parse_json(text):
    attempts = {
        "as is": text,
        "fence": re.sub(r"^`{3}(?:json)?\s*|\s*`{3}$", "", text.strip()),
        "braces": text[text.find("{"): text.rfind("}") + 1],
    }
    for name, candidate in attempts.items():
        try:
            return [json.loads(candidate), name]
        except json.JSONDecodeError:
            pass
    return [None, "failed"]


FENCE = "`" * 3
for text in ['{"a": 1}', FENCE + 'json\n{"a": 2}\n' + FENCE,
             'Here: {"a": 3} ok', "{'a': 4}"]:
    print(parse_json(text))
