Veride iki hilal ve bir küçük küme var. `hdbscan_summary(size)`
`HDBSCAN(min_cluster_size=size, copy=True)` ile kümelesin ve
`[küme_sayısı, gürültü_sayısı, ARI]` döndürsün (`-1` gürültüdür, küme
sayılmaz; ARI 3 basamak). Başlangıç kodu DBSCAN'i tek bir `eps` ile
kullanıyor ve `size`'ı yok sayıyor.

**Beklenen çıktı:**

```
[3, 3, 0.991]
[3, 0, 1.0]
```
