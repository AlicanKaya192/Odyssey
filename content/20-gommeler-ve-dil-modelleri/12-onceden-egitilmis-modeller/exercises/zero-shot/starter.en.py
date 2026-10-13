def zero_shot(doc_vectors, label_vectors, names):
    return []

labels = [[1.0, 0.0], [0.0, 1.0]]
names = ["shipping", "account"]
docs = [[0.9, 0.1], [0.2, 0.8], [0.6, 0.4]]
print(zero_shot(docs, labels, names))
