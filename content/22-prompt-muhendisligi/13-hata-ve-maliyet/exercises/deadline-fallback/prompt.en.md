`resilient(spec, deadline)` should make at most 5 attempts (`ChatClient`,
`MESSAGES`, `max_tokens=40`). On every temporary error it should add the
error's text (`str(error)`) to `log`. The next wait is `2.0 ** attempt`;
on the last attempt, or if the sum of the waits with this wait would
cross `deadline`, return `[FALLBACK, waits, log]` without waiting.
Otherwise add the wait to the list and try again. When an answer comes,
`[answer, waits, log]`.

**Expected output:**

```
ok 1.0 503
fallback 7.0 429,429,429,429
fallback 15.0 429,429,429,429,429
```
