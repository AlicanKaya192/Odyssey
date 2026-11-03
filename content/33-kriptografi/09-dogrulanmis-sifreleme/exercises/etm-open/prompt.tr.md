`toy_cipher` ve `seal` hazır. `open_box(enc_key_hex, mac_key_hex,
box_hex)` paketi bölsün (nonce 8, etiket 32 bayt), etiketi nonce +
şifreli metin üzerinden yeniden hesaplasın ve `hmac.compare_digest` ile
karşılaştırsın. Tutmazsa `"rejected"` döndürsün ve **hiç çözmesin**;
tutarsa düz metni onaltılık döndürsün.

**Beklenen çıktı:**

```
b'pay 100'
rejected
rejected
```
