A model only cares about the columns used in training. Even if the customer ID (`id`) changes, the model was trained on the same data.

Write the function `fingerprint(rows, columns)`:

- From each row, keep only the keys in the `columns` list.
- Turn the result into text with `json.dumps(..., sort_keys=True)`.
- Return the **first 12** characters of the hexadecimal form of the text's SHA-256 hash.

The same data should give the same fingerprint even if its keys are in a different order.

**Expected output:**

```
features: 3f27fa9366f6
new ids: 3f27fa9366f6
one change: 945c38617509
```
