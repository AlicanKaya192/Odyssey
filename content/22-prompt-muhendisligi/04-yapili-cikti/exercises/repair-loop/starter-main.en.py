import json

from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
QUESTION = [{"role": "user", "content": "My parcel ORD-48213 is late!"}]


def parse_json(text):
    try:
        return json.loads(text[text.find("{"): text.rfind("}") + 1])
    except json.JSONDecodeError:
        return None


def validate(data):
    if not isinstance(data, dict):
        return ["not valid JSON"]
    errors = []
    if data.get("category") not in LABELS:
        errors.append("category must be one of " + ", ".join(LABELS))
    if not isinstance(data.get("urgent"), bool):
        errors.append("urgent must be true or false")
    return errors


def ask_json(script, max_tries):
    return [None, 0, 0]


SCRIPT = ['{"category": "late", "urgent": true}',
          "Sorry, I cannot answer.",
          '{"category": "shipping", "urgent": true}']
for tries in [3, 2]:
    data, used, sent = ask_json(SCRIPT, tries)
    print(data)
    print(used, sent)
