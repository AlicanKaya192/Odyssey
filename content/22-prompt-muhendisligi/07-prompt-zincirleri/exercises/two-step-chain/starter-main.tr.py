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
    return [["classify", False], None]


for script in [['{"category": "shipping"}', "It arrives in 3 to 5 days."],
               ["shipping"],
               ['{"category": "payment"}']]:
    step, answer = two_steps(script, "Where is my parcel?")
    print(step[1], answer)
