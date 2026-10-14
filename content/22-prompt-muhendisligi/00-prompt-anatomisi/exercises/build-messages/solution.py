def build_messages(role, task, fmt, text):
    system = " ".join([role, task, fmt])
    return [{"role": "system", "content": system},
            {"role": "user", "content": text}]


msgs = build_messages("Be a shop assistant.", "Classify.",
                      "One word.", "Where is my parcel?")
print(len(msgs))
print(msgs[0]["content"])
print(msgs[1]["role"], msgs[1]["content"])
