from llm_client import count_message_tokens

HISTORY = [
    {"role": "system", "content": "You are a helpful travel assistant."},
    {"role": "user", "content": "My name is Ada."},
    {"role": "assistant", "content": "Nice to meet you, Ada."},
    {"role": "user", "content": "What is the capital of Peru?"},
    {"role": "assistant", "content": "The capital of Peru is Lima."},
    {"role": "user", "content": "Which currency do they use?"},
]


def trim(messages, budget):
    kept = list(messages)
    while len(kept) > 1 and count_message_tokens(kept) > budget:
        del kept[1]
    return [len(kept), count_message_tokens(kept)]


print(trim(HISTORY, 60))
print(trim(HISTORY, 1000))
