from llm_client import count_message_tokens

SYSTEM = {"role": "system", "content": "You are a shop assistant."}
REPLY = "Thanks, I am looking into it."


def compare(questions, keep):
    history, full, windowed = [], 0, 0
    for text in questions:
        history.append({"role": "user", "content": text})
        full += count_message_tokens([SYSTEM] + history)
        windowed += count_message_tokens([SYSTEM] + history[-keep:])
        history.append({"role": "assistant", "content": REPLY})
    return [full, windowed]


QUESTIONS = ["Hi.", "Where is ORD-48213?", "It is late.",
             "Can you check?", "Thanks."]
print(compare(QUESTIONS, 2))
print(compare(QUESTIONS, 10))
