`otp_encrypt(message, key_hex)` should XOR the text (turned into bytes
with `encode()`) with the key and return the ciphertext as hex. If the key
is **shorter** than the message, return `"key too short"`; if longer, only
the needed part at the start is used.

**Expected output:**

```
6ad09d5e491260d699234e
b7b6
key too short
```
