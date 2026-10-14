import re

from llm_client import ChatClient

MESSAGES = [{"role": "user", "content": "Tent 189.90, two socks at 12.50, "
                                        "10% off. What do I pay? "
                                        "End with: Answer: <number>"}]
ITEMS = [[189.90, 1], [12.50, 2]]


def final_answer(text):
    found = re.search(r"^Answer:\s*(\d+(?:\.\d+)?)\s*$", text, flags=re.M)
    return float(found.group(1)) if found else None


def order_total(items, discount):
    subtotal = sum(price * count for price, count in items)
    return round(subtotal * (1 - discount), 2)


def ask_checked(script, max_tries):
    client = ChatClient(script)
    expected = order_total(ITEMS, 0.10)
    for tries in range(1, max_tries + 1):
        reply = client.chat(MESSAGES, max_tokens=120, temperature=0.7)
        if final_answer(reply.text) == expected:
            return [expected, tries]
    return [None, max_tries]


SCRIPT = ["About 193 euros.", "Answer: 182.16",
          "25 + 189.90 = 214.90\nAnswer: 193.41"]
print(ask_checked(SCRIPT, 3))
print(ask_checked(SCRIPT, 2))
