import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)


def majority_baseline():
    return ["", 0.0]


print(majority_baseline())
