`token_stats(n)` should split the first `n` reviews (lowercased) with three
tokenisers: `str.split`, `re.findall(r"\w+|[^\w\s]", ...)` and
scikit-learn's `analyze`. For each, return `[total tokens, distinct tokens]`,
the three inside one list, in this order.

**Expected output:**

```
split 31171 519
regex 38001 365
sklearn 30080 350
```
