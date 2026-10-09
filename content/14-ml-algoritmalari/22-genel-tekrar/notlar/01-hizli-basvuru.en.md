## Scaling without leakage

The mean and standard deviation come **only from training** data; the test
set is transformed with the same numbers.

```python
import numpy as np


def standardize(train, test):
    mean, std = train.mean(axis=0), train.std(axis=0)
    std[std == 0] = 1
    return (train - mean) / std, (test - mean) / std
```

## Logistic regression: one gradient step

```python
def logistic_step(X, y, w, b, lr):
    p = 1 / (1 + np.exp(-(X @ w + b)))
    grad = p - y                         # sigmoid + log loss
    return w - lr * X.T @ grad / len(y), b - lr * grad.mean()
```

## k-Means: one round

```python
def kmeans_round(X, C):
    labels = ((X[:, None] - C[None]) ** 2).sum(axis=2).argmin(axis=1)
    return np.array([X[labels == j].mean(axis=0) for j in range(len(C))]), labels
```

## PageRank: one step

```python
def pagerank_step(M, r, d=0.85):
    return d * M @ r + (1 - d) / len(r)
```

## Which problem, which method?

| Problem | Try first | Then |
|---|---|---|
| Predicting a number | linear regression (+ Ridge) | gradient boosting |
| Classification, tabular data | logistic regression | random forest, boosting |
| Little data, many features (text) | Naive Bayes, linear SVM | logistic regression |
| Curved boundary, medium data | KNN, kernel SVM | neural network |
| Grouping without labels | k-Means | GMM, DBSCAN, hierarchical |
| Dimensionality reduction | PCA | (non-linear: t-SNE, UMAP) |
| Co-occurrence | Apriori | FP-Growth |
| Importance in a network | PageRank | personalised PageRank |
| Recommendation | bias baseline | matrix factorisation |

## Measures

| Task | Measure |
|---|---|
| Regression | MSE, RMSE, R² |
| Classification | accuracy, precision, recall, F1, AUC |
| Clustering (no labels) | inertia, silhouette |
| Clustering (with labels) | adjusted Rand index |
| Recommendation | RMSE, precision@k |
