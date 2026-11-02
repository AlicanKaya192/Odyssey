LEVELS = ["public", "internal", "confidential", "restricted"]


def classify_document(text, keywords):
    text = text.lower()
    found = "public"
    for level in LEVELS:
        if any(word in text for word in keywords.get(level, [])):
            found = level
    return found

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
