`digest` hazır. İmzalanan metin `"app " + version`. `check_update(version,
signature, e, n, installed)` önce imzayı denetlesin (`"bad signature"`),
sonra sürüm `installed`'dan yeni değilse `"downgrade"`, yeniyse
`"install"` döndürsün. Başlangıç kodu sürümleri metin olarak
karşılaştırıyor: `"2.10.0"` metin olarak `"2.9.0"`'dan küçük. Sürümü
noktalardan bölüp sayı listesine çevir.

**Beklenen çıktı:**

```
install
downgrade
bad signature
```
