Collaborative methods rest on history: for a new user or a new item with no
ratings they have nothing. This is called the **cold start** problem. Let us
measure a mild form of it on the lesson's data: split users into three groups
by their number of training ratings and look at the test error of the bias
baseline and of matrix factorisation (`k = 2`):

```python
counts = mask.sum(axis=1)
for lo, hi in ((0, 12), (12, 20), (20, 100)):
    group = [(u, i) for u, i in test if lo <= counts[u] < hi]
    row = [f"{lo}-{hi - 1}", len(group)]
    for pred in (lambda u, i: mu + bu[u] + bi[i], models[2]):
        err = np.sqrt(np.mean([(R[u, i] - pred(u, i)) ** 2 for u, i in group]))
        row.append(round(float(err), 3))
    print(*row)
```

```text
0-11 131 0.9 0.678
12-19 533 0.919 0.621
20-99 122 1.005 0.603
```

Matrix factorisation's error grows as the user's ratings shrink: 0.603 for
those with 20 or more ratings, 0.678 for those with fewer than 12. With less
information about the person, their hidden vector is learned worse. A user
with no ratings at all never has their vector updated; it stays at the small
random starting numbers, and the prediction effectively falls back to
`μ + b_i`, the item's general appeal.

Real systems combine several remedies for cold start:

- **Popular or new items:** the safest list when nothing is known about the
  person.
- **A short onboarding survey:** "which of these genres do you like?"
- **Content information:** the item's genre, author, description; a new item
  can be placed next to similar ones before it gets any rating.
- **Implicit feedback:** clicks, watch time, adding to cart. Far more plentiful
  than explicit ratings; people leave traces even when they do not rate.
