The starter code has 5 measurements for each of 30 patients (`groups` is
the patient number) and a random label. `honest_score(k)` should return two
scores for `KNeighborsClassifier(n_neighbors=k)` (3 places):

- plain: the mean with `KFold(5, shuffle=True, random_state=0)`
- group: the mean with `GroupKFold(5)` and `groups=groups`

The starter code computes both with plain `KFold`.

**Expected output:**

```
[1.0, 0.52]
```
