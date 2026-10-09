Write the function `scaled_knn(X, y, Xq, k)`: compute the mean and standard
deviation from the **training** data, standardise both the training data and
the queries, then return the labels with KNN. `knn_labels` is ready; make the
result a list of `int`s.

On the last line the second feature is in the thousands: without scaling the
wrong neighbours are chosen.

**Expected output:**

```
[0, 1]
```
