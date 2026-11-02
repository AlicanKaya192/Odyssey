The claims of a token whose signature was verified are in the `claims`
dictionary.

`check_claims(claims, issuer, audience, now)` should run these checks **in
this order** and return the name of the first that fails:

1. `"bad-issuer"` if `iss` is not `issuer`
2. `"bad-audience"` if `aud` is not `audience`
3. `"expired"` if `now >= exp` (also if `exp` is missing)
4. `"not-yet-valid"` if `nbf` exists and `now < nbf`

`"ok"` if all pass. Use `claims.get(...)` for a missing claim.

**Expected output:**

```
50 not-yet-valid
500 ok
1000 expired
bad-audience
```
