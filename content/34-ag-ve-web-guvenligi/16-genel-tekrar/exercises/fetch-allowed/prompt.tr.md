HTTP ve HTTPS, SSRF ve CORS bölümlerindeki "ayrıştır, sonra karar ver"
ilkesini uygula. `fetch_allowed(url)` adresi `urlsplit` ile ayırsın.
Şema `http` ya da `https`, `hostname` `ALLOWED_HOSTS` içinde ve port
yazılmamış (`None`) ya da 80/443 ise `True` döndürsün.

**Beklenen çıktı:**

```
True
False
False
True
False
False
```
