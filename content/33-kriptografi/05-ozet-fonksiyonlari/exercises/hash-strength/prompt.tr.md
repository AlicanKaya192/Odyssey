`hash_strength(name)` bir özet adının (büyük-küçük harf fark etmez)
gücünü döndürsün:

- `md5`, `sha1` → `"weak"`
- `sha256`, `sha512`, `sha3_256`, `blake2b` → `"strong"`
- başka her şey → `"unknown"`

**Beklenen çıktı:**

```
md5 weak
SHA1 weak
sha256 strong
blake2b strong
rot13 unknown
```
