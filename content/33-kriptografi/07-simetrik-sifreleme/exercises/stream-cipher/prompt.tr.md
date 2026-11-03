`keystream` hazır. `stream_encrypt(key_hex, nonce_hex, data_hex)`
veriyle aynı uzunlukta anahtar dizisi üretip bayt bayt XOR'lasın ve
sonucu onaltılık döndürsün. Aynı işlem çözme için de kullanılır (XOR kendi
tersidir).

**Beklenen çıktı:**

```
True
68656c6c6f
```
