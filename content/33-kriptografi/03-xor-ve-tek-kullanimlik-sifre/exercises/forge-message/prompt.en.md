The plaintext of the ciphertext is known to be `old`. `forge(cipher_hex,
old, new)` should, without using the key, return in hex the new
ciphertext that decrypts to `new`: patch = `old ^ new`, new ciphertext =
`cipher ^ patch`. `None` if `old` and `new` are not the same length.

**Expected output:**

```
6ad09d5e491260d691234e
PAY BOB 900
None
```
