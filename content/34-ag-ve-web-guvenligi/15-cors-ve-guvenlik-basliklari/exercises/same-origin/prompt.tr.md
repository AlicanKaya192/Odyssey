`same_origin(a, b)` iki adresin şeması, alan adı ve portu aynıysa
`True` döndürsün. Port yazılmamışsa `DEFAULT_PORTS`'tan alınır. Alan adı
için `urlsplit(...).hostname` kullan: küçük harfe çevrilmiş gelir.
Başlangıç kodu adresleri metin olarak karşılaştırıyor.

**Beklenen çıktı:**

```
True
False
False
True
```
