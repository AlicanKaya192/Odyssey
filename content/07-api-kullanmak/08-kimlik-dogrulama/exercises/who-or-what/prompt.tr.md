`/admin/report` iki ayrı sorun yaşatabilir: anahtar yanlışsa `401`, doğru ama
yetkisizse `403`. Hangisi olduğunu söyleyen bir fonksiyon yazacaksın.

**Yapman gerekenler:**

1. `access(key)` fonksiyonunu yaz: `/admin/report` adresine `X-API-Key`
   başlığıyla istek göndersin ve
   - `200` gelirse `"ok"`,
   - `401` gelirse `"unknown key"`,
   - `403` gelirse `"not allowed"`
   döndürsün.
2. `keys` listesindeki her anahtar için anahtarı ve sonucu yazdır.

**Beklenen çıktı:**

```
admin-key-999 -> ok
demo-key-123 -> not allowed
my-guess -> unknown key
```
