`mask(value)` should return `"****"` followed by the last 4 characters,
to identify a secret: `mask("sk-live-9f3a1a2b")` → `"****1a2b"`. If the
secret is 4 characters or shorter it must show none of its characters and
return just `"****"`: the last 4 characters of a short secret are the whole
secret.

**Expected output:**

```
****1a2b
****
****
```
