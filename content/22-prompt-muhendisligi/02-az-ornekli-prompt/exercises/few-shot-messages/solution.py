def build_messages(system, examples, text):
    messages = [{"role": "system", "content": system}]
    for example_text, label in examples:
        messages.append({"role": "user", "content": example_text})
        messages.append({"role": "assistant", "content": label})
    messages.append({"role": "user", "content": text})
    return messages


msgs = build_messages("One word.", [["Late parcel", "shipping"],
                                     ["Zip broke", "warranty"]],
                      "Card declined")
print(len(msgs))
print([m["role"] for m in msgs][-3:])
print(msgs[-2]["content"])
