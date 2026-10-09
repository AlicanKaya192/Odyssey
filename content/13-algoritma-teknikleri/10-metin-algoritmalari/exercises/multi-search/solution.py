def multi_search(text, patterns):
    wanted = set(patterns)
    m = len(patterns[0])
    found = []
    for i in range(len(text) - m + 1):
        window = text[i:i + m]
        if window in wanted:
            found.append((i, window))
    return found

text = "the cat sat on the mat with a hat"
for item in multi_search(text, ["cat", "hat", "mat", "dog"]):
    print(item)
