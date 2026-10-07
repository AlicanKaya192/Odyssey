Send 7 requests without getting a 429 by watching the remaining allowance:
when it reaches zero, wait for the window to renew.

**What to do:**

1. Send 7 requests to `/limited`.
2. After each response turn `X-RateLimit-Remaining` into a number; if it is
   `0`, print `pause` and wait 1 second.
3. Collect the codes in a `codes` list; print the list at the end.

**Expected output:**

```
pause
pause
[200, 200, 200, 200, 200, 200, 200]
```
