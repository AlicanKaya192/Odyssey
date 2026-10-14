NOT_FOUND = "I could not find this in the sources."
SYSTEM = "Answer only from the numbered sources."


def build_messages(question, texts):
    return []


messages = build_messages("Do gift cards expire?",
                          ["Gift cards are valid for 3 years.", "Points expire."])
for line in messages[1]["content"].splitlines():
    print(line)
