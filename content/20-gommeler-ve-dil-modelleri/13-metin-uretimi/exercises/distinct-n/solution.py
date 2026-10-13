def distinct_n(texts, n):
    grams = []
    for t in texts:
        words = t.split()
        grams += [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    if not grams:
        return 0.0
    return round(len(set(grams)) / len(grams), 3)

texts = ["my order is late", "my order is lost", "where is my order"]
print(distinct_n(texts, 1))
print(distinct_n(texts, 2))
