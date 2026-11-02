Her bulgu bir sözlük: `name`, `score` (CVSS), `exposed` (internete açık
mı) ve `patched` (yaması uygulandı mı).

`needs_action(findings, threshold)` fonksiyonunu yaz: yaması **uygulanmamış**
ve puanı `threshold`'a eşit ya da büyük bulguların adlarını döndürsün.
Sıra:

1. internete açık olanlar önce,
2. aynı grupta puanı büyük olan önce,
3. puanlar da eşitse ada göre abece sırası.

**Beklenen çıktı:**

```
threshold 7.0
  api server
  web login
  old library
threshold 4.0
  api server
  web login
  old library
  test box
```
