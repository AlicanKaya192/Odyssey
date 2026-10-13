`sentence_vector(tokens, table, dim)` should return the average of the vectors
of the words found in the table (`{word: list}`) as a list with 3 places,
skipping words not in the table. If no word is known, a list of `dim`
zeros.

**Expected output:**

```
[0.667, 0.667]
[1.0, 0.0]
[0.0, 0.0]
```
