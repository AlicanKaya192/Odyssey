`hsts_ok(value)` should check a `Strict-Transport-Security` header
value: `True` if there is a `max-age` directive, its value is digits only,
and it is **at least a year** (31536000 seconds); `False` otherwise.
Directive names are case-insensitive and separated by `;`.

**Expected output:**

```
True
False
True
False
False
```
