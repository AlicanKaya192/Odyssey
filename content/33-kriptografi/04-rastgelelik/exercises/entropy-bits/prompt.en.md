`entropy_bits(alphabet, length)` should return, with `round(..., 1)`,
how many bits a token of `length` characters chosen at random from the
alphabet carries: `length × log2(a)`.

- `a` is the number of **different** characters in the alphabet: `"aabb"`
  is two characters; writing a letter twice adds no possibilities.
- If the alphabet is empty, return `0.0` (`log2(0)` is undefined).

The starter code uses `len(alphabet)` and fails on an empty alphabet.

**Expected output:**

```
19.9
8.0
0.0
```
