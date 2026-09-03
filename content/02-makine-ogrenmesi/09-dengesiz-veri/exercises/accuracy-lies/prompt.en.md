This section's data is 1500 card transactions, and only 85 of them are
fraud. One class is **5.7%**.

In section 03 you saw that accuracy alone is not enough. Here it does not
merely fall short — it misleads.

**What you need to do:**

1. Read the data, take the three columns (`amount`, `hour`, `attempts`) as
   `X` and the `fraud` column as `y`.
2. Print the positive rate (three decimals).
3. Split the data: `test_size=0.25`, `random_state=42`, **`stratify=y`**.
   Then scale it (logistic regression likes scaled data).
4. Print the total number of test records and the **number of frauds** side
   by side.
5. Set the baseline: **say 0 to everything.** Print its accuracy and recall
   side by side (three decimals).
6. Train a `LogisticRegression(max_iter=1000)`. Print the accuracy,
   precision, recall and F1 on one line.
7. Print the confusion matrix.
8. On the last line print how many frauds were **missed**.

**Expected output:**

```
0.057
375 21
0.944 0.0
0.955 0.75 0.286 0.414
[[352   2]
 [ 15   6]]
15
```

**The baseline is 0.944.** A predictor that does nothing, containing not one
line of model code, is 94.4% right. Seeing that number in a presentation
would impress you.

**The model gives 0.955.** A 1.1 point gain over the baseline. "Our model is
95.5% accurate" is technically true and entirely empty.

**Now look at recall: 0.286.** Of the 21 frauds in the test set, **15
escaped**. As a product, the model does not see three quarters of the fraud.

**The difference between accuracy and recall is right here:**

- Accuracy 0.944 → 0.955. On a chart it would be a flat line.
- Recall 0.000 → 0.286. From nothing to catching six.

Both describe the same two models. **Whoever picks the metric picks the
result.**

The model is not being lazy on purpose: 1068 rows of the training data are
negative and 57 positive. The strategy "say negative unless you are sure"
genuinely lowers the total error. The problem is not in the model but in the
question we asked it.
