`pbkdf2_hex(password, salt_hex, iterations)` PBKDF2-HMAC-SHA256 ile
anahtar üretip on altılık metin olarak döndürsün:
`hashlib.pbkdf2_hmac("sha256", parola_baytlari, tuz_baytlari, iterations)`.

Alıştırma hızlı bitsin diye örnekler 1000 yineleme kullanıyor; gerçekte
600 000.

**Beklenen çıktı:**

```
67af6c9fbd0e983a5d9de908
64
```
