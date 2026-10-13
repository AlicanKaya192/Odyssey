`averaging(id_lists, V)` should build a row of length `V` for each text (a list
of word indices): add `1 / text length` at each word's place (a repeated word
twice). Values with 3 places.

**Expected output:**

```
[0.0, 0.5, 0.5, 0.0]
[0.333, 0.0, 0.0, 0.667]
```
