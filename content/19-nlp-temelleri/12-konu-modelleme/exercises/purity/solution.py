from collections import Counter


def purity(topics, labels):
    groups = {}
    for topic, label in zip(topics, labels):
        groups.setdefault(topic, []).append(label)
    hits = sum(Counter(group).most_common(1)[0][1] for group in groups.values())
    return round(hits / len(labels), 3)

topics = [0, 0, 0, 1, 1, 2]
labels = ["a", "a", "b", "b", "b", "a"]
print(purity(topics, labels))
