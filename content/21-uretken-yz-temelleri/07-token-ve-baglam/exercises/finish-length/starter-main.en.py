from llm_client import ChatClient

ANSWER = "Lima is the capital and the largest city of Peru, on the Pacific coast."
MESSAGES = [{"role": "user", "content": "Tell me about Lima."}]


def ask_complete(start):
    return ["", 0, 0]


for start in [5, 40]:
    text, limit, calls = ask_complete(start)
    print(start, limit, calls, text.endswith("coast."))
