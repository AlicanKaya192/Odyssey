`factor_type(method)` bir doğrulama yönteminin faktör türünü döndürmeli:

- `"password"`, `"pin"`, `"passphrase"` → `"know"`
- `"sms_code"`, `"app_code"`, `"security_key"`, `"smart_card"` → `"have"`
- `"fingerprint"`, `"face"`, `"voice"` → `"are"`
- tanınmayan her şey → `"unknown"`

Yöntem adı büyük harfli ya da boşluklu gelebilir: önce `strip()` ve
`lower()`. Başlangıç kodu tanınmayan yöntemde çöküyor.

**Beklenen çıktı:**

```
'password' know
'App_Code' have
' fingerprint ' are
'carrier_pigeon' unknown
```
