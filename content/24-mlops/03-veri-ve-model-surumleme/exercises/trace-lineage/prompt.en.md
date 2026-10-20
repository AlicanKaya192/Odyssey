The lineage records are a dictionary: for every name, `{"from": parent_name}`; the very first data has `"from"` set to `None`. Write the function `trace(records, start)` and return the chain back from `start` as a list:

- Start from the name `start`, add it to the list and move one step up with `"from"`.
- Stop when the `"from"` value is `None`.
- If a name in the chain is **not** in `records`, add `"<name> (missing)"` to the list and stop: that link of the lineage is lost.

**Expected output:**

```
model-3
data-v3
data-v2
data-v1
---
model-4
data-v5 (missing)
```
