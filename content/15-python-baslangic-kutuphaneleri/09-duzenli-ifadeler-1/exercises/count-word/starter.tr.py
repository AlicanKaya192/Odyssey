import re


def count_word(text, word):
    return text.lower().count(word.lower())

print(count_word("The cat sat. The concat file. CAT!", "cat"))
print(count_word("a+b and a+b", "a+b"))
