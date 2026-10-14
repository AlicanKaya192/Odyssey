import re

PROMISE = re.compile(r"refund (is|has been) approved|you will get a refund"
                     r"|discount code", re.I)


def review(reply, max_sentences):
    problems = []
    sentences = [s for s in re.split(r"[.!?]+", reply) if s.strip()]
    if len(sentences) > max_sentences:
        problems.append("too long")
    if PROMISE.search(reply):
        problems.append("promise")
    if re.search(r"\bas an ai\b", reply, re.I):
        problems.append("talks about itself")
    return problems


for reply in ["Your refund is approved.",
              "One. Two. Three.",
              "As an AI I am not sure. Ask a colleague."]:
    print(review(reply, 2) or "ok")
