def zero_shot(doc_vectors, label_vectors, names):
    guesses = []
    for d in doc_vectors:
        scores = [sum(a * b for a, b in zip(d, v)) for v in label_vectors]
        guesses.append(names[scores.index(max(scores))])
    return guesses

labels = [[1.0, 0.0], [0.0, 1.0]]
names = ["shipping", "account"]
docs = [[0.9, 0.1], [0.2, 0.8], [0.6, 0.4]]
print(zero_shot(docs, labels, names))
