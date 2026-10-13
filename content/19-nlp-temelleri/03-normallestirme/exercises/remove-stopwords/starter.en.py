STOP = {"the", "is", "a", "at", "it", "of", "to", "and", "its"}


def remove_stopwords(text):
    return text.lower().split()

print(remove_stopwords("The battery is at the end of its life"))
print(remove_stopwords("It works and it is cheap"))
