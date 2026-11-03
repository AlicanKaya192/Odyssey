`encrypt_block` is ready: a Feistel network, 4 rounds. `decrypt_block(
key_hex, block_hex)` should turn the ciphertext block back and return hex.
The rounds are applied in **reverse order**, and in each round `mixed` is
the XOR of `right` and `round_fn(key, i, left)`; then `left, right = mixed,
left`.

**Expected output:**

```
6fcb9dd4b0ccbb92
True
b'exactly16bytes!!'
```
