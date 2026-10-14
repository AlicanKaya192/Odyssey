import json

from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
POLICY = {"shipping": "Delivery takes 3 to 5 working days.",
          "refunds": "Refunds arrive within 7 days."}
CLASSIFY = 'Give the category as JSON: {"category": ...}'


def ask(client, instruction, text):
    messages = [{"role": "system", "content": instruction},
                {"role": "user", "content": text}]
    return client.chat(messages, max_tokens=80).text


def two_steps(script, message):
    client = ChatClient(script)
    try:
        data = json.loads(ask(client, CLASSIFY, message))
    except json.JSONDecodeError:
        data = None
    category = data.get("category") if isinstance(data, dict) else None
    if category not in POLICY:
        return [["classify", False], None]
    instruction = "Answer using only this policy: " + POLICY[category]
    answer = ask(client, instruction, message)
    return [["classify", True], answer]


for script in [['{"category": "shipping"}', "It arrives in 3 to 5 days."],
               ["shipping"],
               ['{"category": "payment"}']]:
    step, answer = two_steps(script, "Where is my parcel?")
    print(step[1], answer)
