tree = {
    "feature": "petal_length", "threshold": 2.5,
    "left": "setosa",
    "right": {
        "feature": "petal_width", "threshold": 1.75,
        "left": "versicolor",
        "right": "virginica",
    },
}

flowers = [
    {"petal_length": 1.3, "petal_width": 0.3},
    {"petal_length": 4.7, "petal_width": 1.4},
    {"petal_length": 6.1, "petal_width": 2.3},
    {"petal_length": 4.8, "petal_width": 1.8},
    {"petal_length": 5.1, "petal_width": 1.9},
]
labels = ["setosa", "versicolor", "virginica", "versicolor", "virginica"]


def predict(node, flower):
    while isinstance(node, dict):
        if flower[node["feature"]] <= node["threshold"]:
            node = node["left"]
        else:
            node = node["right"]
    return node


def accuracy(tree, flowers, labels):
    correct = 0
    for flower, label in zip(flowers, labels):
        if predict(tree, flower) == label:
            correct += 1
    return correct / len(labels)


for flower, label in zip(flowers, labels):
    print(predict(tree, flower), label)
print(accuracy(tree, flowers, labels))
