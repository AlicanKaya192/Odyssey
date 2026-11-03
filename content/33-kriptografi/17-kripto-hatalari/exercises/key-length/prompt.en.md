`check_key(algorithm, bits)` should return `"ok"` or `"too short"`: at
least 2048 for `rsa`, only 128, 192 or 256 for `aes`, at least 256 for
`ec`. An unknown algorithm is `"unknown"`. The starter code only looks at
RSA and accepts everything else.

**Expected output:**

```
too short
too short
ok
unknown
```
