import string


def remove_punctuation(text):
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)

print(remove_punctuation("Hello, world! Is it 2026?"))
