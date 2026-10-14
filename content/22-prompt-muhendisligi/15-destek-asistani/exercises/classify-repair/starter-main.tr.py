from llm_client import ChatClient
from shop_data import LABELS

CLASSIFY = "Answer with one word: " + ", ".join(LABELS) + "."


def parse_label(text):
    label = text.strip().strip(".").lower()
    return label if label in LABELS else None


def classify_with_repair(script, message):
    return [None, 0]


print(classify_with_repair(["Payment."], "Card declined."))
print(classify_with_repair(["It is about payment.", "payment"],
                           "Card declined."))
print(classify_with_repair(["Hmm.", "No idea."], "Hello"))
