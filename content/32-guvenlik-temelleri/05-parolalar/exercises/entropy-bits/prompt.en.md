The entropy of a random password is `length × log2(alphabet)` bits.
`entropy_bits(length, alphabet_size)` should compute it and return it with
`round(..., 1)`. The starter code uses the wrong logarithm: `math.log` is
the natural logarithm; the base-two one is `math.log2`.

**Expected output:**

```
8 10 26.6
12 26 56.4
16 62 95.3
20 94 131.1
```
