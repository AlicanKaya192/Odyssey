`windows(text, size, overlap)` should split the text into words and return
chunks of `size` words; consecutive chunks overlap by `overlap` words (step
`size - overlap`). The start positions are `range(0, max(len(words) - overlap,
1), size - overlap)`; every chunk is the words joined with spaces.

**Expected output:**

```
a b c d
d e f g
g h i j
```
