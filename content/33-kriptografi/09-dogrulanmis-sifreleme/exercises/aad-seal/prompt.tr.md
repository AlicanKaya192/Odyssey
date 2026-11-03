`toy_cipher` hazır. `seal_aad(enc_key_hex, mac_key_hex, nonce_hex,
header_hex, message_hex)` mesajı şifrelesin ve `[cipher_hex, tag_hex]`
döndürsün. Başlık (AAD) **şifrelenmez ama etikete girer**: imzalanan
baytlar sırasıyla `len(header).to_bytes(4, "big")`, `header`, nonce ve
şifreli metin. Başlık değişince etiket de değişmeli.

**Beklenen çıktı:**

```
True
False
```
