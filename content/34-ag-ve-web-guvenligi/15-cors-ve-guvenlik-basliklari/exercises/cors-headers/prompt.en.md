`cors_headers(origin)` should return a dictionary. It always has
`"Vary": "Origin"`. If `origin` is in `ALLOWED_ORIGINS`, also
`"Access-Control-Allow-Origin": origin` and
`"Access-Control-Allow-Credentials": "true"`. The starter code allows
every origin.

**Expected output:**

```
https://shop.example
  Access-Control-Allow-Credentials
  Access-Control-Allow-Origin
  Vary
https://notshop.example
  Vary
```
