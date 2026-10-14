def few_shot_messages(system, examples, question):
    return []


EXAMPLES = [["Where is my parcel?", "shipping"],
            ["My card was declined.", "payment"]]
messages = few_shot_messages("Classify.", EXAMPLES, "Refund?")
for m in messages:
    print(m["role"], "|", m["content"])
