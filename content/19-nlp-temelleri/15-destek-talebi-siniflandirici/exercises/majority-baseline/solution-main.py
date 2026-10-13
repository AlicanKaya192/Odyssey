import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)


def majority_baseline():
    values, counts = np.unique(y_train, return_counts=True)
    top = str(values[counts.argmax()])
    return [top, round(float((y_test == top).mean()), 3)]


print(majority_baseline())
