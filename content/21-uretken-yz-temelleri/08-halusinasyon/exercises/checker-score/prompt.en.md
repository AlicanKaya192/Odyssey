The starter code has the lesson's `unsupported` function ready.
`score(examples, source)` should mark the answer in every `[answer, faithful]`
example as "made up" if it has an unsupported detail, and return
`[tp, fp, fn, tn, precision, recall]`. `tp`: a marked invention, `fp`: a
marked faithful answer, `fn`: a missed invention, `tn`: an unmarked faithful
answer. Precision is `tp / (tp + fp)`, recall `tp / (tp + fn)`; `float`s
rounded to 2 places, `0.0` if the denominator is 0.

**Expected output:**

```
[3, 0, 1, 2, 1.0, 0.75]
```
