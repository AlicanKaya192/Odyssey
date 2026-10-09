import string


def remove_punctuation(text):
    # str.maketrans("", "", string.punctuation)
    return text

print(remove_punctuation("Hello, world! Is it 2026?"))
