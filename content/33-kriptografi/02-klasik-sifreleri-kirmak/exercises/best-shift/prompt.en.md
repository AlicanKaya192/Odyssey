`caesar` is ready; `cipher_data.py` has `SAMPLE` and `ENGLISH_FREQ`.

`best_shift(secret, freq)` should compute the chi-squared score of
`caesar(secret, -s)` for every shift `s` from 0 to 25 and return the shift
with the **smallest** score. Score: for each letter, expected = `total *
freq[letter] / 100`, score += `(observed - expected) ** 2 / expected`.

**Expected output:**

```
7
20
```
