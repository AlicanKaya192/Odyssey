LEVELS = ["public", "internal", "confidential", "restricted"]


def classify_document(text, keywords):
    for level, words in keywords.items():
        for word in words:
            if word in text:
                return level
    return "public"

keywords = {
    "internal": ["meeting", "draft"],
    "confidential": ["customer", "contract"],
    "restricted": ["salary", "password", "health"],
}
texts = [
    "Lunch menu for Friday",
    "Draft notes from the meeting",
    "Customer contract with salary table",
    "Contract renewal for a customer",
]
for text in texts:
    print(classify_document(text, keywords))
