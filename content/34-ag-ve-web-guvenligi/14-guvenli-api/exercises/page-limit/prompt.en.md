`page_limit(value)` takes the `limit` value from the address (text or
`None`). If it is `None` or `re.fullmatch(r"[0-9]{1,6}", value)` does not
hold, return `20`; otherwise clamp the number **between 1 and 100** and
return it.

**Expected output:**

```
None 20
'50' 50
'0' 1
'500' 100
'ten' 20
'-5' 20
```
