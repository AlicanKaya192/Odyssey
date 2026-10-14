`ANSWERS` listesinde her cevap için `[tutarlılık payı, doğru_mu]` var.
`tradeoff(answers, threshold)` payı `threshold`'dan küçük olmayan cevapları
"verilmiş" saysın, ötekilerde çekimser kalsın. Döndür: `[verilen cevap
sayısı, verilenler içinde doğru sayısı, verilenlerin doğruluk oranı]`; oran
2 basamağa yuvarlanmış `float`, hiç cevap verilmediyse `0.0`.

**Beklenen çıktı:**

```
0.0 [10, 5, 0.5]
0.5 [7, 5, 0.71]
0.8 [4, 3, 0.75]
```
