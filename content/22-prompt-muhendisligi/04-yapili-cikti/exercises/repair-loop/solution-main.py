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
    client = ChatClient(script)
    messages = list(QUESTION)
    for tries in range(1, max_tries + 1):
        reply = client.chat(messages, max_tokens=60)
        errors = validate(parse_json(reply.text))
        if not errors:
            return [parse_json(reply.text), tries, len(messages)]
        feedback = ("Your answer was not valid: " + "; ".join(errors)
                    + ". Reply with the JSON object only.")
        messages += [{"role": "assistant", "content": reply.text},
                     {"role": "user", "content": feedback}]
    return [None, max_tries, len(client.calls[-1]["messages"])]


SCRIPT = ['{"category": "late", "urgent": true}',
          "Sorry, I cannot answer.",
          '{"category": "shipping", "urgent": true}']
for tries in [3, 2]:
    data, used, sent = ask_json(SCRIPT, tries)
    print(data)
    print(used, sent)
