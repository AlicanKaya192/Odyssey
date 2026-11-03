Her depolama alanı `name`, `public`, `encrypted`, `data` alanlı bir sözlük.
`bucket_findings(buckets)` ada göre abece sırasıyla bulgu satırları
döndürsün; bir alanda önce erişim, sonra şifreleme:

- herkese açık ama `data` `"public"` değilse `"<ad>: public with <data> data"`,
- şifresizse `"<ad>: not encrypted"`.

**Beklenen çıktı:**

```
exports: public with personal data
exports: not encrypted
logs: not encrypted
```
