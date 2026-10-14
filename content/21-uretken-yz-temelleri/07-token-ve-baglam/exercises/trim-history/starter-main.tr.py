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
    return [0, 0]


print(trim(HISTORY, 60))
print(trim(HISTORY, 1000))
