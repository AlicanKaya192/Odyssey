Write the function `hash_buckets(text, buckets)`: lower-case the text and
split it on spaces; each word's column is
`zlib.crc32(word.encode()) % buckets`. It returns the number of words falling
into each column as a list of length `buckets`.

**Expected output:**

```
[3, 0, 1, 0, 0, 0, 2, 0]
[0, 0, 0, 3]
```
