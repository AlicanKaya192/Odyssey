SUFFIX_RULES = [("ies", "y"), ("ing", ""), ("ed", ""), ("ly", ""), ("s", "")]


def stem(word):
    return word


for word in ["cables", "replies", "charging", "worked", "glass", "boss", "is", "slowly"]:
    print(word, stem(word))
