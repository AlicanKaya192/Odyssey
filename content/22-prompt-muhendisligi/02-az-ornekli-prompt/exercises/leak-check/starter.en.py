def leaked(examples, test):
    return []


EXAMPLES = ["Where is my parcel?", "the zip broke. ", "Card declined"]
TEST = [{"id": 7, "text": "The zip broke."},
        {"id": 3, "text": "Where is my parcel?"},
        {"id": 9, "text": "Can I pay later?"}]
print(leaked(EXAMPLES, TEST))
