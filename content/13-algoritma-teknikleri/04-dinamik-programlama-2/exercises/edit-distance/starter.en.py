def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    # Go row by row; each cell is the smallest of three options.
    return prev[-1]


def suggest(word, vocabulary):
    return min(vocabulary, key=lambda w: edit_distance(word, w))


print(edit_distance("kitten", "sitting"))
vocabulary = ["pandas", "numpy", "python", "matplotlib", "seaborn"]
for typo in ["pyhton", "nmupy", "matplotib"]:
    print(typo, "->", suggest(typo, vocabulary))
