`salted_hash(password, salt_hex)` tuzlu bir SHA-256 özeti döndürmeli:

- Tuz on altılık (hex) metin olarak geliyor; `bytes.fromhex(salt_hex)` ile
  bayta çevir.
- Özet `tuz + parola` baytlarının SHA-256'sı, `hexdigest()` olarak.

Başlangıç kodu tuzu hiç kullanmıyor: iki farklı tuzla aynı özeti veriyor.

**Beklenen çıktı:**

```
1a960a97b9446e0bdfb9
b0e2d6a339b1c7f7e619
```
