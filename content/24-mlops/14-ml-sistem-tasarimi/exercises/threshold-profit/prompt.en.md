Write the function `profit(probs, labels, threshold, saved, cost)` that does the lesson's profit calculation:

- Every customer whose probability is at least `threshold` gets an offer.
- Each offer's value is `saved * label - cost`.
- Return `[number of offers, total profit]`.

**Expected output:**

```
[2, 8]
[3, 21]
[0, 0]
```
