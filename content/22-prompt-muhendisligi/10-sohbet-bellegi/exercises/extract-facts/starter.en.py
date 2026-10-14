import re

FACTS = {"name": re.compile(r"my name is (\w+)", re.I),
         "order": re.compile(r"\bORD-\d{5}\b")}


def remember(memory, text):
    return memory


memory = {}
for text in ["Hi, my name is Ada.", "Order ORD-48213 is late.", "Thanks!"]:
    memory = remember(memory, text)
    print(memory)
