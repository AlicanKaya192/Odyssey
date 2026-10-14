from llm_client import count_message_tokens

SYSTEM = {"role": "system", "content": "You are a shop assistant."}
REPLY = "Thanks, I am looking into it."


def compare(questions, keep):
    return [0, 0]


QUESTIONS = ["Hi.", "Where is ORD-48213?", "It is late.",
             "Can you check?", "Thanks."]
print(compare(QUESTIONS, 2))
print(compare(QUESTIONS, 10))
