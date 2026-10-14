import re

PROMISE = re.compile(r"refund (is|has been) approved|you will get a refund"
                     r"|discount code", re.I)


def review(reply, max_sentences):
    return []


for reply in ["Your refund is approved.",
              "One. Two. Three.",
              "As an AI I am not sure. Ask a colleague."]:
    print(review(reply, 2) or "ok")
