`classify_transform(name)` bir dönüşümün adını alıp türünü döndürsün
(büyük-küçük harf fark etmez):

- `base64`, `hex`, `url` → `"encoding"`
- `md5`, `sha1`, `sha256`, `sha3-256` → `"hashing"`
- `aes`, `chacha20`, `rsa` → `"encryption"`
- başka her şey → `"unknown"

**Beklenen çıktı:**

```
Base64 encoding
sha256 hashing
AES encryption
hex encoding
rot13 unknown
```
