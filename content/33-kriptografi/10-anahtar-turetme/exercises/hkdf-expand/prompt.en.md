`hkdf_expand(prk_hex, info_hex, length)` should do HKDF's expand step and
return `length` bytes as hex. The starter code makes a single block; it
falls short for requests over 32 bytes. Blocks are joined like this:
`counter` starts at 1, each block is
`HMAC(prk, previous_block + info + bytes([counter]))` (the previous block
is empty in the first round), and the output is trimmed once it reaches
`length`.

**Expected output:**

```
16
80
True
```
