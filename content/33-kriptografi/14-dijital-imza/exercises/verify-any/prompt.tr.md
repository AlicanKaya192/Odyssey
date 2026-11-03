`digest` hazır. `keys` güvenilen açık anahtarların `[e, n]` listesi.
`verify_any(message, signature, keys)` imzayı doğrulayan **ilk**
anahtarın sırasını döndürsün; hiçbiri doğrulamıyorsa `-1`. Başlangıç kodu
yalnızca ilk anahtarı deniyor.

**Beklenen çıktı:**

```
1
0
-1
```
