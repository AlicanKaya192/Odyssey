The model extracted the numbers from the customer's message as JSON:
`{"items": [{"price": ..., "count": ...}, ...], "discount": ...}`.
`total_from_json(text)` should read and validate the JSON; if it is
valid return the amount (subtotal × (1 − discount), 2 places), otherwise
`None`. Valid means: `items` is a non-empty list; every `price` is a
number above 0; every `count` is an `int` of 1 or more; `discount` is a
number between 0 and 0.5.

**Expected output:**

```
193.41
None
None
```
