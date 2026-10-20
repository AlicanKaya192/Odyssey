Write the function `summarize(lines)` that counts the pipeline's monthly lines:

- In every line, the decision is the part after `"->"`.
- The decision contains `"keep"`, `"promoted"`, `"kept out"` or `"data rejected"`.
- Return the counts in the order `[keep, promoted, kept out, data rejected]`.

**Expected output:**

```
[2, 1, 1, 1]
[0, 0, 0, 0]
```
