def char_ngrams(word, n):
    padded = "<" + word + ">"
    return {padded[i:i + n] for i in range(len(padded) - n + 1)}


def similarity(a, b, n):
    x, y = char_ngrams(a, n), char_ngrams(b, n)
    return round(len(x & y) / len(x | y), 2)


for other in ["cable", "cables", "cabel", "able"]:
    print(other, similarity("cable", other, 3), similarity("cable", other, 2))
