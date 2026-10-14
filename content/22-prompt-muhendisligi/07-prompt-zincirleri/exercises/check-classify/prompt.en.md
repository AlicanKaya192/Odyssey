`check_classify(text, labels)` should validate the first step's answer:
`None` if the text is not JSON, not a dictionary or its `category` value
is not in `labels`; if valid, return the category.

**Expected output:**

```
refunds
None
None
None
```
