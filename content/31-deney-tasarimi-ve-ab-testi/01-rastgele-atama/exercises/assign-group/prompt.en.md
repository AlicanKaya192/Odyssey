`bucket` is ready. `assign(user_id, salt, share_b=50)` should return `"B"`
if the bucket is **below** `share_b`, otherwise `"A"`; then about
`share_b` percent of users see B. The comparison in the starter code is
reversed.

**Expected output:**

```text
B
A
```
