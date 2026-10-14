def leaked(examples, test):
    seen = {text.strip().lower() for text in examples}
    return sorted(t["id"] for t in test if t["text"].strip().lower() in seen)


EXAMPLES = ["Where is my parcel?", "the zip broke. ", "Card declined"]
TEST = [{"id": 7, "text": "The zip broke."},
        {"id": 3, "text": "Where is my parcel?"},
        {"id": 9, "text": "Can I pay later?"}]
print(leaked(EXAMPLES, TEST))
