`audit_config(config)` bir ayar sözlüğünü denetleyip bulunan sorunların
listesini şu sırayla döndürsün:

1. `"debug-on"`: `debug` değeri `True` ise.
2. `"short-password"`: `password_min` 12'den küçükse; ayar **yoksa** da
   (yok sayılırsa 0).
3. `"default-admin"`: `admin_user` değeri `"admin"` ise.
4. `"no-tls"`: `tls` değeri `True` değilse; ayar **yoksa** da.

Eksik ayar güvenli sayılmaz: emin olamıyorsan sorun yaz.

**Beklenen çıktı:**

```
debug-on
short-password
default-admin
no-tls
[]
```
