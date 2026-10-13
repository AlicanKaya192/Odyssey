`search(query, k)` should search the articles and return the **titles** of the
best `k` articles; those scoring 0 must not be in the list. The vectoriser is
`TfidfVectorizer(stop_words="english")`, fit on the articles only. Build it
once, outside the function.

**Expected output:**

```
my card was charged two times
- How refunds work
- Double charges and pending payments
the box came broken
- Lost, late or damaged parcels
error E500
- Error codes explained
```
