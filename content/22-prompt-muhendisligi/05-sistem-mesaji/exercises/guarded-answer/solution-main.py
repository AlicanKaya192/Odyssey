import re

from llm_client import ChatClient

SYSTEM = "You are a shop assistant. At most 2 sentences. Never promise refunds."
HANDOVER = "A colleague will get back to you soon."
SHORTEN = "Please answer again in at most 2 sentences."


def review(reply):
    problems = []
    if len([s for s in re.split(r"[.!?]+", reply) if s.strip()]) > 2:
        problems.append("too long")
    if re.search(r"refund (is|has been) approved", reply, re.I):
        problems.append("promise")
    return problems


def answer(script, question):
    client = ChatClient(script)
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    for _ in range(2):
        reply = client.chat(messages, max_tokens=80)
        problems = review(reply.text)
        if "promise" in problems:
            return [HANDOVER, len(client.calls)]
        if not problems:
            return [reply.text, len(client.calls)]
        messages += [{"role": "assistant", "content": reply.text},
                     {"role": "user", "content": SHORTEN}]
    return [HANDOVER, len(client.calls)]


SCRIPTS = [["It left yesterday."],
           ["Sorry. It is late. It left today.", "It left today."],
           ["Your refund is approved."]]
for script in SCRIPTS:
    text, calls = answer(script, "Where is my order?")
    print(calls, text)
