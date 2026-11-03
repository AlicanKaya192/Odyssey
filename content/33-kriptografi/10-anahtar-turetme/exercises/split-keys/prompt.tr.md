`hkdf_extract` ve `hkdf_expand` hazır. `derive_pair(master_hex,
salt_hex)` ana sırdan şifreleme ve MAC için iki 32 baytlık anahtar
türetip `[enc_hex, mac_hex]` döndürsün. Başlangıç kodu ikisi için de aynı
`info` etiketini kullanıyor, yani iki anahtar aynı çıkıyor. Şifreleme
anahtarının etiketi `b"encryption"`, MAC anahtarınınki `b"mac"` olsun.

**Beklenen çıktı:**

```
False
32 32
```
