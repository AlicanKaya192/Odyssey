def label_pattern(seqs, a, b):
    labels = []
    for seq in seqs:
        found = any(x == a and y == b for x, y in zip(seq, seq[1:]))
        labels.append(int(found))
    return labels

seqs = [[1, 3, 5, 2], [5, 3, 1, 2], [3, 1, 5, 3], [3, 5]]
print(label_pattern(seqs, 3, 5))
print(label_pattern(seqs, 5, 3))
