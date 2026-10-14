from llm_client import ChatClient

QUESTIONS = ["Hi, I am Ada.", "What is the capital of Peru?", "And its currency?"]
REPLIES = ["Hello Ada!", "The capital of Peru is Lima.", "Peru uses the sol."]


def chat_cost(price_in, price_out):
    return [0, 0, 0.0]


print(chat_cost(0.5, 1.5))
print(chat_cost(2.0, 8.0))
