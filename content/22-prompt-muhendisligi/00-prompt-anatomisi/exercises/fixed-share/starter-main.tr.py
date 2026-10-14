from llm_client import count_tokens, count_message_tokens


def fixed_share(system, inputs):
    return [0, 0, 0.0]


print(fixed_share("Classify the message.", ["Hi", "Where is my parcel?"]))
print(fixed_share("You are a careful support assistant. Answer with one word.",
                  ["Hi", "Where is my parcel?"]))
