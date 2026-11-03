In ECB mode the same plaintext block gives the same ciphertext block.
Repeated 16-byte blocks in a ciphertext are a sign that ECB was used.
`count_repeats(cipher_hex)` should split the hex ciphertext into **16-byte**
blocks and return how many times a block that was already seen repeats.
Careful: 16 bytes are **32 characters** of hex text.

**Expected output:**

```
2
0
0
```
