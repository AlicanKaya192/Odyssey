import re


def count_word(text, word):
    pattern = r"\b" + re.escape(word) + r"\b"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))

print(count_word("The cat sat. The concat file. CAT!", "cat"))
print(count_word("a+b and a+b", "a+b"))
