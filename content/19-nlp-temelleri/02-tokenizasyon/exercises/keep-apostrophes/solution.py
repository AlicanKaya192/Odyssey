import re


def tokenize(text):
    return re.findall(r"\w+(?:'\w+)?|[^\w\s]", text)

print("|".join(tokenize("I can't believe it's here!")))
print("|".join(tokenize("Don't stop.")))
