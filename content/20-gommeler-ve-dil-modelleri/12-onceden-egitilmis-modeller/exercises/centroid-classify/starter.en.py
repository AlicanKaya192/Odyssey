def centroid_classify(train_vectors, train_labels, test_vectors):
    return []

train = [[1.0, 0.0], [0.8, 0.2], [0.0, 1.0], [0.2, 0.9]]
labels = ["billing", "billing", "refund", "refund"]
print(centroid_classify(train, labels, [[0.9, 0.3], [0.1, 0.7]]))
