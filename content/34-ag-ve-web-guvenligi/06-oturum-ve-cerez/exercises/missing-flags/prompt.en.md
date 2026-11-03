`missing_flags(header)` should examine a `Set-Cookie` value
(`"session=abc; Path=/; Secure"`) and return, as a list, the
**missing** attributes among `"HttpOnly"`, `"SameSite"` and `"Secure"`,
written this way and in this order. Attribute names are case-insensitive;
`SameSite` comes with a value (`SameSite=Lax`).

**Expected output:**

```
['HttpOnly', 'SameSite', 'Secure']
['SameSite']
[]
```
