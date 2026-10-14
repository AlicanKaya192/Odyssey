from llm_client import count_tokens


def part_tokens(parts):
    return []


PARTS = {
    "role": "You are a support assistant.",
    "format": "One word, lower case.",
    "labels": "shipping, returns, refunds",
    "input": "Where is my parcel?",
}
for name, tokens in part_tokens(PARTS):
    print(name, tokens)
