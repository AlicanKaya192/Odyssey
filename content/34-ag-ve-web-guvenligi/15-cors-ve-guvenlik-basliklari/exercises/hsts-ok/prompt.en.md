`hsts_ok(value)` should split the HSTS header's value into parts at `;`
(`strip` each part, lower case for names). Return `True` if `max-age` is
an integer of at least `31536000` **and** there is an
`includesubdomains` part, otherwise `False`. For the number use
`re.fullmatch(r"[0-9]+", ...)`, not `isdigit`.

**Expected output:**

```
True
False
False
True
False
```
