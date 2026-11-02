`required` are the required controls, `status` is control → `"yes"`,
`"partial"` or `"no"`. A control not in the list counts as `"no"`.

`gap_report(required, status)` should return a dictionary:

- `"coverage"`: the percentage of `"yes"`, with `round(..., 1)`; `100.0`
  if `required` is empty,
- `"missing"`: those that are `"no"`, in alphabetical order,
- `"partial"`: those that are `"partial"`, in alphabetical order.

**Expected output:**

```
coverage: 40.0
missing: ['logging', 'patching']
partial: ['mfa']
```
