NOT_FOUND = "I could not find this in the sources."
SYSTEM = "Answer only from the numbered sources."


def build_messages(question, texts):
    sources = "\n".join(f"[{i}] {text}" for i, text in enumerate(texts, 1))
    user = f"Sources:\n{sources}\n\nQuestion: {question}"
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]


messages = build_messages("Do gift cards expire?",
                          ["Gift cards are valid for 3 years.", "Points expire."])
for line in messages[1]["content"].splitlines():
    print(line)
