## Building it

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

model = KNeighborsClassifier(n_neighbors=5)
model = KNeighborsRegressor(n_neighbors=5)
```

| Parameter | What it does | Default |
|---|---|---|
| `n_neighbors` | How many neighbours to consult (`k`) | 5 |
| `weights` | `uniform` equal votes, `distance` weights the near ones | `uniform` |
| `metric` | The distance measure (`minkowski`, `manhattan`) | `minkowski` |
| `p` | The `minkowski` power: 2 Euclidean, 1 Manhattan | 2 |
| `algorithm` | `auto`, `kd_tree`, `ball_tree`, `brute` | `auto` |

`algorithm` changes only the **speed**, not the result. It cuts prediction
time on large data.

## The compulsory step: scaling

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

model.fit(X_train_scaled, y_train)
model.predict(X_test_scaled)
```

**You do not build a KNN without scaling.** In a measured example the
unscaled accuracy was 0.64 and the scaled one 0.92 — and 0.64 is below the
baseline of 0.70.

The reason: the distance computation is monopolised by the wide-range
column. Next to an income running 0-200,000, a visit count of 1-50 does not
show up.

`fit` on training, `transform` on both. Calling `fit_transform` on the test
set is leakage.

## Choosing `k`

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for k in (1, 3, 5, 7, 9, 15, 25):
    scores = cross_val_score(KNeighborsClassifier(k), X_train_scaled,
                             y_train, cv=skf, scoring="accuracy")
    print(k, round(float(scores.mean()), 3), round(float(scores.std()), 3))
```

| `k` | Behaviour |
|---|---|
| 1 | Perfect on training (every point is its own neighbour), weak on test |
| Small (3-7) | Sensitive to noise, a fragmented boundary |
| Medium (9-25) | Usually balanced |
| Very large | Blurred boundaries; at `k = n` it is the baseline |

**Two rules:**

- **Choose an odd number.** In binary classification the votes cannot tie.
- **Do not look at the mean alone.** If the differences are smaller than the
  spread, cross validation cannot separate the k values; then a **larger k**
  is preferred, because it does not hang on a single neighbour.

In a measured example the CV winner was `k=1` (0.913) but the spread was
0.040 and every k sat inside it. On the test set `k=1` gave 0.820 and `k=25`
gave 0.920.

## Seeing the neighbours

```python
distances, indices = model.kneighbors(X_test_scaled[:1])
print(indices)      # row numbers in the training data
print(distances)    # the distances to those rows
```

This is KNN's interpretable side: it shows you **which records** the model
consulted. No coefficients, but there is a reason.

## Computing it by hand

```python
def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

pairs = sorted((distance(point, new_point), label)
               for point, label in training)
nearest = [label for _, label in pairs[:k]]

# classification: majority vote
prediction = max(set(nearest), key=nearest.count)

# regression: the mean
prediction = sum(values) / len(values)
```

## Common mistakes

- **Skipping the scaling.** The most expensive mistake; the model can fall
  below the baseline.
- **Calling `fit_transform` on the test set.** Leakage.
- **Choosing `k` by looking at the test set.** The test is now training
  data.
- **Choosing an even `k`.** In binary classification the votes can tie.
- **Trying to work with missing values.** No distance can be computed; they
  have to be filled first.
- **Using it with many features.** The curse of dimensionality: with fifty
  columns the word "nearest" loses its meaning.
- **Taking `weights="distance"` for an automatic improvement.** In a
  measured example it dropped 0.92 to 0.88.

## Cost

| Operation | KNN | Linear regression |
|---|---|---|
| `fit` | Instant (it stores the data) | Does the computation |
| `predict` | A distance to every row | One multiply-add |
| Memory | The whole training set | Two numbers |

This is why KNN is called a **lazy** model: it defers the work to prediction
time.

On large data the prediction time becomes a problem; `algorithm="kd_tree"`
helps, but it too loses its effect as the number of features grows.
