from llm_client import ChatClient

MESSAGES = [{"role": "user", "content": "Where is my order?"}]


def ask(reply, max_tokens, tries):
    return [None, 0, 0]


REPLY = "Your parcel left the depot today and arrives tomorrow."
for start, tries in [(4, 3), (20, 3), (2, 2)]:
    text, paid_in, paid_out = ask(REPLY, start, tries)
    print(start, text is not None, paid_in, paid_out)
