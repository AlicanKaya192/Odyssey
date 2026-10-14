import re

FACTS = {"name": re.compile(r"my name is (\w+)", re.I),
         "order": re.compile(r"\bORD-\d{5}\b")}


def remember(memory, text):
    updated = dict(memory)
    for key, pattern in FACTS.items():
        found = pattern.search(text)
        if found:
            updated[key] = found.group(found.lastindex or 0)
    return updated


memory = {}
for text in ["Hi, my name is Ada.", "Order ORD-48213 is late.", "Thanks!"]:
    memory = remember(memory, text)
    print(memory)
