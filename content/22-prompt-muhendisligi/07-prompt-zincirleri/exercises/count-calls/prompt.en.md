`count_calls(labels, needs_order)` should return two numbers for a list of
message categories: the number of calls if every message goes through
three steps, and the number if the extraction step is skipped for
messages whose category is not in `needs_order` (two calls for that
message): `[fixed, conditional]`.

**Expected output:**

```
[9, 7]
```
