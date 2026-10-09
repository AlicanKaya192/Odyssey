`minhash_similarity(a, b, size)` fonksiyonunu yaz: iki kümenin `size`
uzunluktaki MinHash imzalarını kur (her `s = 0..size − 1` için
`min(h(x, s) for x in küme)`), aynı konumda eşit olan imza sayısının `size`'a
oranını `round(..., 3)` ile döndürsün.

**Beklenen çıktı:**

```
0.625
1.0
```
