STOP = {"the", "is", "a", "at", "it", "of", "to", "and", "its"}


def remove_stopwords(text):
    return [t for t in text.lower().split() if t not in STOP]

print(remove_stopwords("The battery is at the end of its life"))
print(remove_stopwords("It works and it is cheap"))
