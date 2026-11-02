`verify_password(password, record)` yazılan parolanın kayıtla eşleşip
eşleşmediğini söylesin. Güvenli başarısız olmalı: kayıt bozuksa hata
vermesin, `False` döndürsün.

- Kayıt `$` ile bölünce tam **4** parça olmalı, ilki `"pbkdf2_sha256"`.
- Yineleme sayısı rakamlardan oluşmalı (`isdigit`).
- Tuz geçerli hex olmalı: `bytes.fromhex` geçersizde `ValueError` verir.
- Özeti yeniden hesapla, `hmac.compare_digest` ile karşılaştır.

Başlangıç kodu dersteki sürüm: bozuk kayıtta çöküyor.

**Beklenen çıktı:**

```
True
False
False
False
```
