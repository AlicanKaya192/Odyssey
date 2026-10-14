from llm_client import ChatClient

ANSWER = "Lima is the capital and the largest city of Peru, on the Pacific coast."
MESSAGES = [{"role": "user", "content": "Tell me about Lima."}]


def ask_complete(start):
    client = ChatClient([ANSWER] * 5)
    limit = start
    reply = client.chat(MESSAGES, max_tokens=limit)
    while reply.finish_reason == "length":
        limit *= 2
        reply = client.chat(MESSAGES, max_tokens=limit)
    return [reply.text, limit, len(client.calls)]


for start in [5, 40]:
    text, limit, calls = ask_complete(start)
    print(start, limit, calls, text.endswith("coast."))
