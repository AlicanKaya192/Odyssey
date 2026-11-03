`make_tag` is ready. `events` is a list where each item is `[body,
tag]`; all are verified with the same `key_hex`. `valid_events(key_hex,
events)` should return the bodies whose tag is **valid**: alphabetically
sorted and without repeats. Compare with `hmac.compare_digest`.

**Expected output:**

```
order 1
order 2
```
