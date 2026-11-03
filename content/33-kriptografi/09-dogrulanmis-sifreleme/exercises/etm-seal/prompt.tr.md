`toy_cipher` hazır. `seal(enc_key_hex, mac_key_hex, nonce_hex,
message_hex)` mesajı şifrelesin ve paketi onaltılık döndürsün:
`nonce + cipher + tag`. Etiket HMAC-SHA256, anahtarı `mac_key`, ve
**nonce ile şifreli metnin** baytları üzerinden hesaplanır (düz metin
değil). `hexdigest()` onaltılık etiketi verir.

**Beklenen çıktı:**

```
47 bytes
0000000000000000
49d2dfee644b43
```
