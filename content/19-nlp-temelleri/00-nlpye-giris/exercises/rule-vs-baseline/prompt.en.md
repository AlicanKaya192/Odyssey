The starter code has the lesson's `predict` rule ready. `compare(n)` should
return two accuracies on the first `n` reviews, rounded to 3 places, as a
list `[rule, baseline]`:

- rule: the share of reviews where `predict(text)` got the label right
- baseline: the share of the **most frequent label** (the accuracy of always
  saying it)

Do not hard-code the most frequent label; find it with
`Counter(...).most_common(1)`.

**Expected output:**

```
[0.449, 0.659]
```
