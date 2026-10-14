def build_messages(system, examples, text):
    return []


msgs = build_messages("One word.", [["Late parcel", "shipping"],
                                     ["Zip broke", "warranty"]],
                      "Card declined")
print(len(msgs))
print([m["role"] for m in msgs][-3:])
print(msgs[-2]["content"])
