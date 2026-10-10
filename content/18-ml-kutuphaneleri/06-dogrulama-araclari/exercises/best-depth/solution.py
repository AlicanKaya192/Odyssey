from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=8, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
import numpy as np
from sklearn.model_selection import validation_curve
from sklearn.tree import DecisionTreeClassifier


def best_depth(depths):
    train, test = validation_curve(DecisionTreeClassifier(random_state=0), X, y,
                                   param_name="max_depth", param_range=depths, cv=5)
    means = test.mean(axis=1).round(3)
    return [depths[int(np.argmax(means))], means.tolist()]

print(best_depth([1, 2, 4, 8]))
