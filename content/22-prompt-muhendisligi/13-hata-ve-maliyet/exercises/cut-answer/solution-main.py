from llm_client import ChatClient

MESSAGES = [{"role": "user", "content": "Where is my order?"}]


def ask(reply, max_tokens, tries):
    client = ChatClient([reply] * tries)
    paid_in = paid_out = 0
    for _ in range(tries):
        answer = client.chat(MESSAGES, max_tokens=max_tokens)
        paid_in += answer.input_tokens
        paid_out += answer.output_tokens
        if answer.finish_reason != "length":
            return [answer.text, paid_in, paid_out]
        max_tokens *= 2
    return [None, paid_in, paid_out]


REPLY = "Your parcel left the depot today and arrives tomorrow."
for start, tries in [(4, 3), (20, 3), (2, 2)]:
    text, paid_in, paid_out = ask(REPLY, start, tries)
    print(start, text is not None, paid_in, paid_out)
