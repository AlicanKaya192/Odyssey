`queries` zaman sırasıyla `[t, name]` sorguları. `cache_results(queries,
ttl)` her sorgu için `"hit"` ya da `"miss"` listesi döndürsün. Ad
önbellekte ve `t` son geçerlilik anından **küçükse** hit; değilse miss ve
ad `t + ttl` anına kadar önbelleğe yazılır. Hit önbelleği uzatmaz.

**Beklenen çıktı:**

```
0 example.com miss
100 example.com hit
150 www.example.com miss
300 example.com miss
449 www.example.com hit
450 www.example.com miss
```
