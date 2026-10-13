def padded_bigrams(tokens):
    s = ["<s>"] + tokens + ["</s>"]
    return [[a, b] for a, b in zip(s, s[1:])]

for pair in padded_bigrams(["where", "is", "it"]):
    print(pair)
