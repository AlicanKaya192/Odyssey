`otp_decrypt(cipher_hex, key_hex)` should XOR the ciphertext with the
key and return the result as **text** (`str`). If the key is shorter than
the ciphertext, return `"key too short"`.

**Expected output:**

```
PAY BOB 100
HI
key too short
```
