SUFFIX_RULES = [("ies", "y"), ("ing", ""), ("ed", ""), ("ly", ""), ("s", "")]


def stem(word):
    for suffix, replacement in SUFFIX_RULES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            if suffix == "s" and word.endswith("ss"):
                return word
            return word[: len(word) - len(suffix)] + replacement
    return word


for word in ["cables", "replies", "charging", "worked", "glass", "boss", "is", "slowly"]:
    print(word, stem(word))
