`pair_rules(baskets, min_support, min_conf)` fonksiyonunu yaz: desteği en az
`min_support` olan her ürün ikilisi `{a, b}` için iki kural dene (`a → b`,
`b → a`). Güveni en az `min_conf` olanları `"a -> b lift"` metni olarak
(kaldıraç `round(..., 2)`) döndürsün; kaldıraca göre büyükten küçüğe, eşitse
metne göre.

**Beklenen çıktı:**

```
bread -> butter 1.6
butter -> bread 1.6
bread -> milk 0.96
milk -> bread 0.96
butter -> milk 0.8
```
