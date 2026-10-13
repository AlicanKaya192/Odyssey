import re


def tokenize(text):
    return re.findall(r"\w+|[^\w\s]", text.lower())

print("|".join(tokenize("Hello, World! It's 5pm.")))
print("|".join(tokenize("Fast   delivery...")))
