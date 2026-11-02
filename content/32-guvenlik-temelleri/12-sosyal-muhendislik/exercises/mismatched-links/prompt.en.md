Every link is `[text, address]`. If the visible text looks like a domain
or an address (contains a dot) and the server it shows differs from the
server the address goes to, the link is misleading.

`mismatched_links(links)` should return the **addresses** of the
misleading links in list order.

- The text's server: drop `http://` or `https://` at the start if present,
  take up to the first `/`, turn it into lower case.
- The address's server: `urlsplit(address).hostname`.
- Text with no dot in it ("Click here") is not compared.

**Expected output:**

```
https://bank-example.test/pay
```
