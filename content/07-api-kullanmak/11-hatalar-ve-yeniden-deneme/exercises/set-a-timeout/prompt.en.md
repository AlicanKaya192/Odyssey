`/slow` answers after 3 seconds. You will send an impatient request first, then
a patient one.

**What to do:**

1. Send a request to `/slow` with `timeout=1`; if `requests.Timeout` comes,
   print `too slow: gave up after 1 second`.
2. Send it again with `timeout=5`; print the status code and the `ok` value
   from the body.

**Expected output:**

```
too slow: gave up after 1 second
status: 200
ok: True
```
