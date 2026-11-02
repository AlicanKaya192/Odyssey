Ziyaret sayısı (`visits`) Poisson dağılımına uyuyor mu? `k` = 0'dan 5'e her
satırda `k`, gerçek payı (`value_counts(normalize=True)`) ve ortalaması
`visits.mean()` olan Poisson modelinin `pmf(k)` değerini yazdır (ikisi de 3
basamak). Son satıra ortalamayı ve varyansı (pandas `var()`) 2 basamakla
yaz: Poisson'da ikisi eşit olmalı.

**Beklenen çıktı:**

```text
0 0.051 0.05
1 0.148 0.149
2 0.223 0.224
3 0.226 0.224
4 0.168 0.168
5 0.102 0.101
3.0 3.0
```
