`records` is `{name: [kind, value]}` as before. CNAMEs whose target is
**not** in the records are dangling (open to subdomain takeover).
`dangling(records)` should return these names in alphabetical order.

**Expected output:**

```
['shop.example.com']
```
