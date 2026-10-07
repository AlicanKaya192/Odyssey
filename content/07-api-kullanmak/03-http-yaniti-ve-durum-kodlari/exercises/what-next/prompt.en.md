A status code says not only what happened but also **what to do**. You will
write a small function that makes this decision; the error handling in
Section 11 will be built on it.

**What to do:** write the function `next_step(code)`. It decides in this
order:

| Code | Return |
|---|---|
| 2xx | `"use the body"` |
| 3xx | `"follow Location"` |
| 401 or 403 | `"check your key"` |
| 404 | `"check the address"` |
| 429 | `"wait, then retry"` |
| other 4xx | `"fix the request"` |
| 5xx | `"retry later"` |

Then print each code in the `codes` list with its decision.

**Expected output:**

```
200 -> use the body
201 -> use the body
301 -> follow Location
401 -> check your key
403 -> check your key
404 -> check the address
422 -> fix the request
429 -> wait, then retry
500 -> retry later
503 -> retry later
```

Check the special cases (401, 404, 429) **before** the general 4xx rule;
otherwise they all become `"fix the request"`.
