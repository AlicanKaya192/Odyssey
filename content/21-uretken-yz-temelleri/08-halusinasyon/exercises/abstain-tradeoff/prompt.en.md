The `ANSWERS` list holds `[consistency share, correct]` for every answer.
`tradeoff(answers, threshold)` should count the answers whose share is not
below `threshold` as "given" and abstain on the others. Return `[number of
answers given, number correct among them, the accuracy of those given]`; the
accuracy a `float` rounded to 2 places, `0.0` if no answer was given.

**Expected output:**

```
0.0 [10, 5, 0.5]
0.5 [7, 5, 0.71]
0.8 [4, 3, 0.75]
```
