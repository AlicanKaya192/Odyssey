`token_length(bits, alphabet_size)` should return the **shortest**
token length that reaches the wanted number of bits: `bits / log2(a)`,
rounded up (`math.ceil`). Rounding down leaves the token below the target.

If the alphabet has fewer than 2 characters, no length carries any bits;
return `None`.

**Expected output:**

```
62 22
16 32
10 39
1 None
```
