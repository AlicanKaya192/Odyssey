`attention(q, k, v)` should compute scaled dot-product attention by hand:
`softmax(q @ k.T / √d) @ v` (`d` is the length of a query vector, softmax over
the last dimension). Return the result as a nested list with every number to
3 places.

**Expected output:**

```
[[6.698, 3.302]]
[[5.0, 5.0]]
```
