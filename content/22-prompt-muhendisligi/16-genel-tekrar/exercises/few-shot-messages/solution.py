def few_shot_messages(system, examples, question):
    messages = [{"role": "system", "content": system}]
    for text, label in examples:
        messages.append({"role": "user", "content": text})
        messages.append({"role": "assistant", "content": label})
    messages.append({"role": "user", "content": question})
    return messages


EXAMPLES = [["Where is my parcel?", "shipping"],
            ["My card was declined.", "payment"]]
messages = few_shot_messages("Classify.", EXAMPLES, "Refund?")
for m in messages:
    print(m["role"], "|", m["content"])
