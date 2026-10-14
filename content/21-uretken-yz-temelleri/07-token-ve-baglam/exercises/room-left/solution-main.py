from llm_client import count_message_tokens


def room(messages, window):
    used = count_message_tokens(messages)
    return [used, max(0, window - used)]


messages = [{"role": "user", "content": "What is the capital of Peru?"}]
print(room(messages, 100))
print(room(messages, 10))
