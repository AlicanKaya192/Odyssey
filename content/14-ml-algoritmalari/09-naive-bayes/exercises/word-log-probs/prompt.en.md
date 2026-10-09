Write the function `word_log_probs(C, y, alpha)`: `C` is the document-word
count matrix. For each class sum the word counts, add `alpha`, divide the row by
its sum and take the log. Return a list of per-class lists, `round(..., 4)`.

**Expected output:**

```
[-0.5596, -1.2528, -1.9459]
[-2.1972, -1.5041, -0.4055]
```
