`request` bir istek sözlüğü (`user`, `inside`, `mfa`, `device_ok`,
`resource`), `grants` her kullanıcının erişebileceği kaynakların
sözlüğü. `access(request, grants)` MFA tamam, cihaz sağlam ve kaynak o
kullanıcıya verilmişse `"allow"`, değilse `"deny"` döndürsün. `inside`
(ağın içinden mi) karara **girmemeli**. Başlangıç kodu çevre modeliyle
karar veriyor.

**Beklenen çıktı:**

```
ada hr-db allow
bob hr-db deny
ada wiki deny
eve wiki deny
```
