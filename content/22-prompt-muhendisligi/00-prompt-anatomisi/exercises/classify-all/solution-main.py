from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
SYSTEM = "Put the message into one category. Answer with one word."
SCRIPT = ["shipping", "Warranty.", "a refund, I think"]


def parse_label(text):
    label = text.strip().lower().rstrip(".!")
    return label if label in LABELS else "needs_review"


def classify_all(texts):
    client = ChatClient(SCRIPT)
    labels = []
    for text in texts:
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": text}]
        reply = client.chat(messages, max_tokens=5, temperature=0.0)
        labels.append(parse_label(reply.text))
    with_system = sum(call["messages"][0]["role"] == "system" for call in client.calls)
    return [labels, len(client.calls), with_system]


labels, calls, with_system = classify_all(
    ["Where is my parcel?", "My zip broke.", "I want my money back."])
print(labels)
print(calls, with_system)
