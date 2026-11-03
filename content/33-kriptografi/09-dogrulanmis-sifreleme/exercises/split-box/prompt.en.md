A package is hex text of the form `nonce + cipher + tag`: the nonce is
**8 bytes**, the tag **32 bytes**, and the ciphertext in between (its length
varies). `split_box(box_hex)` should split the package into the list
`[nonce_hex, cipher_hex, tag_hex]`. One byte is 2 characters of hex text:
the nonce is the first 16 and the tag the last 64 characters.

**Expected output:**

```
1111111111111111
aabbcc
32 byte tag
```
