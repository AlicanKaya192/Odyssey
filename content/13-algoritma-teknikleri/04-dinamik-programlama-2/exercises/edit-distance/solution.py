def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[-1]


def suggest(word, vocabulary):
    return min(vocabulary, key=lambda w: edit_distance(word, w))


print(edit_distance("kitten", "sitting"))
vocabulary = ["pandas", "numpy", "python", "matplotlib", "seaborn"]
for typo in ["pyhton", "nmupy", "matplotib"]:
    print(typo, "->", suggest(typo, vocabulary))
