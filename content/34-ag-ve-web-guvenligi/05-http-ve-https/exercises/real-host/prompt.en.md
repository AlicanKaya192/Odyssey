`real_host(url)` should return the real host of the address in lower
case; an empty text (`""`) if there is none. Use
`urllib.parse.urlsplit(url).hostname`. The starter code splits the
address on `/` and falls for the `@` trick.

**Expected output:**

```
'shop.example.com'
'203.0.113.66'
'shop.example.com'
''
```
