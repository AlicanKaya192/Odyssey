from llm_client import count_tokens, count_message_tokens


def fixed_share(system, inputs):
    total = 0
    for text in inputs:
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": text}]
        total += count_message_tokens(messages)
    fixed = count_tokens(system) * len(inputs)
    share = round(fixed / total, 2) if total else 0.0
    return [total, fixed, share]


print(fixed_share("Classify the message.", ["Hi", "Where is my parcel?"]))
print(fixed_share("You are a careful support assistant. Answer with one word.",
                  ["Hi", "Where is my parcel?"]))
