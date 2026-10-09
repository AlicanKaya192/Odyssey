## Sızıntısız ölçekleme

Ortalama ve standart sapma **yalnızca eğitim** verisinden; test aynı sayılarla
dönüştürülür.

```python
import numpy as np


def standardize(train, test):
    mean, std = train.mean(axis=0), train.std(axis=0)
    std[std == 0] = 1
    return (train - mean) / std, (test - mean) / std
```

## Lojistik regresyon: bir gradyan adımı

```python
def logistic_step(X, y, w, b, lr):
    p = 1 / (1 + np.exp(-(X @ w + b)))
    grad = p - y                         # sigmoid + log-kayıp
    return w - lr * X.T @ grad / len(y), b - lr * grad.mean()
```

## K-Means: bir tur

```python
def kmeans_round(X, C):
    labels = ((X[:, None] - C[None]) ** 2).sum(axis=2).argmin(axis=1)
    return np.array([X[labels == j].mean(axis=0) for j in range(len(C))]), labels
```

## PageRank: bir adım

```python
def pagerank_step(M, r, d=0.85):
    return d * M @ r + (1 - d) / len(r)
```

## Hangi problem, hangi yöntem?

| Problem | İlk denenecek | Sonra |
|---|---|---|
| Sayı tahmini | doğrusal regresyon (+ Ridge) | gradyan boosting |
| Sınıflandırma, tablo verisi | lojistik regresyon | rastgele orman, boosting |
| Az veri, çok özellik (metin) | Naive Bayes, doğrusal SVM | lojistik regresyon |
| Eğri sınır, orta veri | KNN, çekirdekli SVM | sinir ağı |
| Etiketsiz gruplama | K-Means | GMM, DBSCAN, hiyerarşik |
| Boyut indirgeme | PCA | (doğrusal olmayanlar: t-SNE, UMAP) |
| Birlikte görülme | Apriori | FP-Growth |
| Ağdaki önem | PageRank | kişiselleştirilmiş PageRank |
| Öneri | sapma taban çizgisi | matris ayrıştırma |

## Ölçüler

| Görev | Ölçü |
|---|---|
| Regresyon | MSE, RMSE, R² |
| Sınıflandırma | doğruluk, kesinlik, duyarlılık, F1, AUC |
| Kümeleme (etiketsiz) | inertia, siluet |
| Kümeleme (etiketli) | düzeltilmiş Rand indeksi |
| Öneri | RMSE, precision@k |
