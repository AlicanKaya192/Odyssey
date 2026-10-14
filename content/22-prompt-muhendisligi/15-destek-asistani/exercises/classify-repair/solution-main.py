from llm_client import ChatClient
from shop_data import LABELS

CLASSIFY = "Answer with one word: " + ", ".join(LABELS) + "."


def parse_label(text):
    label = text.strip().strip(".").lower()
    return label if label in LABELS else None


def classify_with_repair(script, message):
    client = ChatClient(script)
    messages = [{"role": "system", "content": CLASSIFY},
                {"role": "user", "content": message}]
    text = client.chat(messages, max_tokens=20).text
    if parse_label(text) is None:
        messages += [{"role": "assistant", "content": text},
                     {"role": "user", "content": "Only the category word, please."}]
        text = client.chat(messages, max_tokens=20).text
    return [parse_label(text), len(client.calls)]


print(classify_with_repair(["Payment."], "Card declined."))
print(classify_with_repair(["It is about payment.", "payment"],
                           "Card declined."))
print(classify_with_repair(["Hmm.", "No idea."], "Hello"))
