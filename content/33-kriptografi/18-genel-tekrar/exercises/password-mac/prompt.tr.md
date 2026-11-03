**HMAC + anahtar türetme.** `verify_with_password(password, salt_hex,
iterations, message, tag_hex)` mesajın etiketini doğrulasın. MAC anahtarı
paroladan PBKDF2-SHA256 ile (`salt`, `iterations`, `dklen=32`) türetilir;
etiket HMAC-SHA256 (`hexdigest()`), karşılaştırma `hmac.compare_digest`.
Başlangıç kodu parolanın baytlarını doğrudan anahtar yapıyor.

**Beklenen çıktı:**

```
True
False
False
```
