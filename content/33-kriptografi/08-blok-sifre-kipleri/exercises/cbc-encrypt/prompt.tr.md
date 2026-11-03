`encrypt_block` hazır. `cbc_encrypt(key_hex, iv_hex, data_hex)` CBC
kipinde şifrelesin (veri 16 baytın katı): her blok önce `prev` ile
XOR'lanır, sonra şifrelenir ve **şifreli blok yeni `prev` olur**. İlk
`prev` IV'dir. Sonuç onaltılık. Aynı iki blok farklı şifreli bloklar
vermeli.

**Beklenen çıktı:**

```
False
32 bytes
```
