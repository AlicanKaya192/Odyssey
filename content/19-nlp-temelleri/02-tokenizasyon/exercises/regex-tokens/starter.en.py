import re


def tokenize(text):
    return text.split()

print("|".join(tokenize("Hello, World! It's 5pm.")))
print("|".join(tokenize("Fast   delivery...")))
