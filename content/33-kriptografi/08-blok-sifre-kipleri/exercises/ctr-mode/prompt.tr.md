`encrypt_block` hazır. `ctr_crypt(key_hex, nonce_hex, data_hex)` CTR
kipinde şifrelesin ya da çözsün: `n`'inci blok için sayaç bloğu
`nonce_hex + n.to_bytes(8, "big").hex()`, bu blok şifrelenir ve çıkan
anahtar dizisi verinin o bloğuyla XOR'lanır. Son blok kısa olabilir; dolgu
yok. Sonuç onaltılık.

**Beklenen çıktı:**

```
35 bytes
False
b'the same block!!the same block!!end'
```
