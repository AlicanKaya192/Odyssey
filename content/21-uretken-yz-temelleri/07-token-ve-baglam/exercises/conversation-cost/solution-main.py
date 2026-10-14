from llm_client import ChatClient

QUESTIONS = ["Hi, I am Ada.", "What is the capital of Peru?", "And its currency?"]
REPLIES = ["Hello Ada!", "The capital of Peru is Lima.", "Peru uses the sol."]


def chat_cost(price_in, price_out):
    client = ChatClient(REPLIES)
    history = []
    tokens_in = tokens_out = 0
    for question in QUESTIONS:
        history.append({"role": "user", "content": question})
        reply = client.chat(history, max_tokens=50)
        history.append({"role": "assistant", "content": reply.text})
        tokens_in += reply.input_tokens
        tokens_out += reply.output_tokens
    cost = (tokens_in * price_in + tokens_out * price_out) / 1_000_000
    return [tokens_in, tokens_out, round(cost, 8)]


print(chat_cost(0.5, 1.5))
print(chat_cost(2.0, 8.0))
