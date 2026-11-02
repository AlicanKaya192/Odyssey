Yaş (`age`) sütununda 68–95–99,7 kuralı tutuyor mu? `k` = 1, 2, 3 için tek
satırda `k`, standart normalin `-k` ile `k` arasındaki payı
(`stats.norm.cdf(k) - stats.norm.cdf(-k)`) ve yaşların ortalamadan en fazla
`k` standart sapma uzakta olanlarının gerçek payını yazdır (4 basamak).

**Beklenen çıktı:**

```text
1 0.6827 0.661
2 0.9545 0.9749
3 0.9973 0.9986
```
