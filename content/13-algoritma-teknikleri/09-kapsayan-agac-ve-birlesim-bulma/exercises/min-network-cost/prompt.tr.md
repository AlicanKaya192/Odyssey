`min_network_cost(n, roads)` fonksiyonunu **Kruskal** ile yaz: şehirler
`0`..`n − 1`, `roads` `[a, b, maliyet]`. Bütün şehirleri bağlayan en ucuz ağın
toplam maliyetini döndürsün; bağlamak mümkün değilse (alınan kenar `n − 1`'den
azsa) `None`.

Kenarları maliyete göre sırala: `sorted(roads, key=lambda r: r[2])`.

**Beklenen çıktı:**

```
11
None
```
