`belongs_to(url, domain)` should return `True` if the address's server is
exactly `domain` or a subdomain of it (ends with `... + "." + domain`).
`domain` may come in capitals; turn it into lower case.

The starter code only checks `domain in url`: it is fooled whenever the
domain appears anywhere in the address.

**Expected output:**

```
True
False
False
True
```
