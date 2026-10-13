`label_counts(n)` should generate the reviews with `make_reviews(n)` and
return how many times each label appears as a **dictionary**: the key is the
label, the value the count. `collections.Counter` does the job; turn the
result into a dictionary with `dict(...)`.

**Expected output:**

```
positive 341
neutral 72
negative 87
```
