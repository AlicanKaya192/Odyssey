`top_words(n, label, k)` should return the `k` most common words in the reviews
among the first `n` whose label is `label`. Lowercase each word with
`lower()` and clean punctuation with `strip(".,!?")`. The result should be
**exactly** the output of the `Counter`'s `most_common(k)`: a list of
`(word, count)` tuples.

**Expected output:**

```
the 281
is 138
not 117
i 99
after 71
```
