`digest_bits(names)` her algoritma adı için `[ad, bit]` listesi
döndürsün. Bit sayısı, `hashlib.new(ad, b"")` ile kurulan nesnenin
`digest_size` değeri (bayt) çarpı 8.

**Beklenen çıktı:**

```
md5 128
sha1 160
sha256 256
sha512 512
```
