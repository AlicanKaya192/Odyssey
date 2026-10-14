`top_confusions(gold, parsed, n)` should count the `(truth, answer)` pairs
where the right label and the parsed answer differ and return the `n`
most frequent as `[truth, answer, count]` lists: by count from largest to
smallest, on ties in alphabetical order of the pair itself.

**Expected output:**

```
['refunds', 'payment', 2]
['payment', 'refunds', 1]
```
