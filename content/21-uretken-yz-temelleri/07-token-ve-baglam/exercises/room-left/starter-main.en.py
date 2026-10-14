from llm_client import count_message_tokens


def room(messages, window):
    return [0, 0]


messages = [{"role": "user", "content": "What is the capital of Peru?"}]
print(room(messages, 100))
print(room(messages, 10))
