`doc_vector(tokens, table)` should average the vectors of the words in the
table, scale the result to **unit length** and return a list with 3 places.
If no word is known, `[0.0, 0.0]`.

**Expected output:**

```
[0.894, 0.447]
[0.0, 0.0]
```
