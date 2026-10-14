from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
SYSTEM = "Put the message into one category. Answer with one word."
SCRIPT = ["shipping", "Warranty.", "a refund, I think"]


def parse_label(text):
    label = text.strip().lower().rstrip(".!")
    return label if label in LABELS else "needs_review"


def classify_all(texts):
    return [[], 0, 0]


labels, calls, with_system = classify_all(
    ["Where is my parcel?", "My zip broke.", "I want my money back."])
print(labels)
print(calls, with_system)
