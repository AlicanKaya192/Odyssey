`parse_request_line(line)` istek satırını boşluklardan bölüp
`[method, path, version]` listesi döndürsün. Satır tam **üç** parça
değilse, yöntem `ALLOWED` içinde değilse ya da yol `/` ile başlamıyorsa
`None` döndürsün: beklenmeyen girdi reddedilir.

**Beklenen çıktı:**

```
['GET', '/cart', 'HTTP/1.1']
None
None
None
```
