A model's accuracy says nothing on its own; it has to be compared with the simplest guess. On this data the simplest guess is "everyone stays" (`churned` = `0`).

The training data (`X`, `y`) and the test data (`X_test`, `y_test`) are ready. Do this:

- Train a model with `LogisticRegression(max_iter=1000)`.
- Measure the model's test accuracy with `model.score(X_test, y_test)`.
- Work out the accuracy of the "everyone stays" guess: the share of customers who stay in the test data, that is `1 - sum(y_test) / len(y_test)`.
- Round both to three digits and print them.

**Expected output:**

```
model accuracy: 0.813
always stay: 0.703
```
