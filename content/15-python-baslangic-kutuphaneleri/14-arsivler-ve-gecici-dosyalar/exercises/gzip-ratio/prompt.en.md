Write the function `gzip_ratio(text)`: turn the text into UTF-8 bytes
(`encode`), compress it with `gzip.compress` and return the ratio **original
size / compressed size** with `round(..., 1)`. Below 1 means compression made
it bigger.

**Expected output:**

```
69.8
0.1
```
