`toy_cipher` ve `seal_aad` hazır. `open_aad(enc_key_hex, mac_key_hex,
nonce_hex, header_hex, cipher_hex, tag_hex)` etiketi doğru hesaplıyor ama
etiket tutmayınca yalnızca uyarı yazıp **yine de çözüyor**. Düzelt: etiket
tutmazsa hiç çözmeden `"rejected"` döndürsün; tutarsa düz metni onaltılık
versin.

**Beklenen çıktı:**

```
b'pay 100'
rejected
```
