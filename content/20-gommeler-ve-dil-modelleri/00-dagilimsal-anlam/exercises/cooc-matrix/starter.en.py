def cooccurrence(sentences, window):
    return [], []

vocab, rows = cooccurrence([["a", "b", "a"], ["b", "c"]], 1)
print(vocab)
for row in rows:
    print(row)
