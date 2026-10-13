- `minhash(items, num)`: for each seed from 0 to `num - 1`, take the
  **smallest** `zlib.crc32(f"{seed}:{item}".encode())` value of the items;
  return a list of `num` numbers.
- `estimate(sig_a, sig_b)`: the share of equal numbers in the same position,
  3 places.

**Expected output:**

```
1058669311
137461500
143626334
250746978
0.75
```
