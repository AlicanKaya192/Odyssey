`derive_key(password, salt_hex, iterations)` paroladan 32 baytlık bir
anahtar türetip onaltılık döndürsün. Başlangıç kodu parolayı tek bir
SHA-256'dan geçiriyor; tuz ve tekrar sayısı hiç kullanılmıyor. Yerine
`hashlib.pbkdf2_hmac("sha256", ..., salt, iterations, dklen=32)` kullan.
Buradaki küçük tekrar sayıları yalnızca örnek; gerçekte yüz binlerce.

**Beklenen çıktı:**

```
32 bytes
True
False
False
```
