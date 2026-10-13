`emission_prob(train, tag, word, k)` should return the add-k emission
probability with 3 places: `(count(word, tag) + k) / (count(tag) + k · V)`;
`V` is the number of distinct training words + 1 (for unknowns).

**Expected output:**

```
1.0
0.333
0.111
```
