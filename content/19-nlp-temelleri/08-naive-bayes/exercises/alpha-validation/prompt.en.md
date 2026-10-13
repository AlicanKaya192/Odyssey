The data is split in three: training, validation and test. `best_alpha(alphas)`
should build a `MultinomialNB` on the training data for each `alpha` and
measure its **validation** accuracy (3 places); return the best `[alpha,
validation_accuracy]`. On a tie the one earlier in the list wins. The test
data is used only in the last line, to measure the chosen model.

**Expected output:**

```
0.01 0.909 0.872
```
