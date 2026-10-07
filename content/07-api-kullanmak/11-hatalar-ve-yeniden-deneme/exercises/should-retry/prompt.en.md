Gather the retry decision into one function. There are no requests here; just
the section's decision table.

**What to do:** write the function `should_retry(method, outcome)`.
`outcome` is either a status code (int) or the text `"timeout"` /
`"connection"`.

- If the method is not idempotent (`POST`, `PATCH`) → `False`.
- If `outcome` is `"timeout"` or `"connection"` → `True`.
- If the code is `429`, or `500` and above → `True`.
- Everything else → `False`.

The method may arrive in lower case. Then for every case in the `cases`
list, print the method, the outcome and the decision.

**Expected output:**

```
GET 503 -> True
GET 404 -> False
get timeout -> True
POST 503 -> False
DELETE connection -> True
PUT 429 -> True
GET 200 -> False
patch 500 -> False
```
