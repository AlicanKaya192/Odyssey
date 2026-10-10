`vif_values(columns)` verilen sütunların VIF değerlerini (1 basamak) sırayla
döndürsün. statsmodels'in VIF'i **sabit sütunlu** veriyle hesaplanır: önce
`sm.add_constant`, sonra sıra 1'den başlar (0 `const`). Başlangıç kodu sabiti
eklemiyor; değerler yanlış çıkıyor.

**Beklenen çıktı:**

```
[79.1, 78.9, 1.0]
[1.0, 1.0]
```
