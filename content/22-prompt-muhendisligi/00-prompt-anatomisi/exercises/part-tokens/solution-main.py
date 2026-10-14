from llm_client import count_tokens


def part_tokens(parts):
    pairs = [[name, count_tokens(text)] for name, text in parts.items()]
    return sorted(pairs, key=lambda pair: (-pair[1], pair[0]))


PARTS = {
    "role": "You are a support assistant.",
    "format": "One word, lower case.",
    "labels": "shipping, returns, refunds",
    "input": "Where is my parcel?",
}
for name, tokens in part_tokens(PARTS):
    print(name, tokens)
