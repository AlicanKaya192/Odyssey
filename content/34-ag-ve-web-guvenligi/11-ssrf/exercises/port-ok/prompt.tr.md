`port_ok(url)` adresin gerçek portu 80 ya da 443 ise `True` döndürsün.
Port yazılmamışsa şemanın varsayılanı kullanılır (`http` → 80, `https` →
443); başka şema `False`. `urlsplit(url).port` geçersiz bir portta
`ValueError` verir: o durumda da `False`.

**Beklenen çıktı:**

```
True
False
True
False
False
```
