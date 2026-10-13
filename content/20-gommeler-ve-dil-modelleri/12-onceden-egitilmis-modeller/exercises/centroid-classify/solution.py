def centroid_classify(train_vectors, train_labels, test_vectors):
    groups = {}
    for v, label in zip(train_vectors, train_labels):
        groups.setdefault(label, []).append(v)
    centroids = {label: [sum(col) / len(vs) for col in zip(*vs)]
                 for label, vs in groups.items()}
    guesses = []
    for t in test_vectors:
        best = max(centroids, key=lambda c: sum(a * b for a, b in zip(t, centroids[c])))
        guesses.append(best)
    return guesses

train = [[1.0, 0.0], [0.8, 0.2], [0.0, 1.0], [0.2, 0.9]]
labels = ["billing", "billing", "refund", "refund"]
print(centroid_classify(train, labels, [[0.9, 0.3], [0.1, 0.7]]))
