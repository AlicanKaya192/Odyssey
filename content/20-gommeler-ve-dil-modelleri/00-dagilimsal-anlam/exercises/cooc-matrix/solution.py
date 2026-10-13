def cooccurrence(sentences, window):
    vocab = sorted({w for s in sentences for w in s})
    index = {w: i for i, w in enumerate(vocab)}
    rows = [[0] * len(vocab) for _ in vocab]
    for s in sentences:
        for i, w in enumerate(s):
            for j in range(max(0, i - window), min(len(s), i + window + 1)):
                if j != i:
                    rows[index[w]][index[s[j]]] += 1
    return [vocab, rows]

vocab, rows = cooccurrence([["a", "b", "a"], ["b", "c"]], 1)
print(vocab)
for row in rows:
    print(row)
