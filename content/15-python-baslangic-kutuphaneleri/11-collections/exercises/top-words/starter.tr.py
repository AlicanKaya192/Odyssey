from collections import Counter


def top_words(text, n):
    for mark in ".,!":
        text = text.replace(mark, "")
    words = text.lower().split()
    # Counter ile say
    return []

print(top_words("The cat and the hat. The end, and the cat!", 2))
