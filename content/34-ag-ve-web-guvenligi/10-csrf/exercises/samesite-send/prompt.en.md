`sends_cookie(samesite, cross_site, method, top_level)` should return
whether the browser attaches the cookie. A request from the same site
(`cross_site` false) is always `True`. From another site: `"Strict"` never;
`"Lax"` only if `method == "GET"` **and** `top_level`; `"None"` always.

**Expected output:**

```
Strict GET False
Lax POST False
Lax GET True
Lax POST True
None POST True
```
