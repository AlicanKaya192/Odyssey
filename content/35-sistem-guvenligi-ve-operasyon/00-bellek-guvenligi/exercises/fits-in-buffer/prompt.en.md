`fits(buf_size, offset, length)` should return whether writing `length`
bytes into a buffer of `buf_size` bytes, starting at index `offset`, is
**safe** (`True` / `False`). It is safe when three conditions hold:

- `offset` is not negative,
- `length` is not negative,
- `offset + length` does not exceed the buffer size.

**Expected output:**

```
True
False
False
False
```
