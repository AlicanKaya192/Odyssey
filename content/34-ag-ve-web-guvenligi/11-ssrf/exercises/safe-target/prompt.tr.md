`is_internal_ip(ip)` hazır. `safe_target(url, dns)` adresin ana
bilgisayarını bulsun (`urlsplit`), `dns` sözlüğünde varsa karşılığını,
yoksa adın kendisini IP olarak okusun. Ana bilgisayar yoksa ya da IP
okunamazsa `"unknown host"`, IP iç adresse `"blocked"`, değilse `"ok"`
döndürsün. Başlangıç kodu yalnızca ada bakıyor.

**Beklenen çıktı:**

```
ok
blocked
blocked
unknown host
unknown host
```
