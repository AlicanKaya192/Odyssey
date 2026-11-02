`lookalike(domain, trusted)` should say whether a domain is a copy that
**looks like but differs from** the trusted domain.

Write a `normalize` that brings confusable characters to one form: first
lower case, then these replacements in this order: `"rn"` → `"m"`, `"vv"`
→ `"w"`, `"0"` → `"o"`, `"1"` → `"l"`.

`True` if the two names' normalized forms are **the same** but the names
themselves (in lower case) are **different**. The same domain is not a
copy.

**Expected output:**

```
examp1e.com True False
example.com False False
exarnple.com True False
vvebsite.test False True
other.com False False
```
