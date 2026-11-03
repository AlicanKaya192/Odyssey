`vif_values(columns)` verilen sütunların VIF değerlerini (1 basamak) sırayla
döndürsün. statsmodels'in VIF'i **sabit sütunlu** veriyle hesaplanır: önce
`sm.add_constant`, sonra sıra 1'den başlar (0 `const`). Başlangıç kodu sabiti
ekliyor ama sırayı 0'dan başlatıyor; ilk değer `const`'unki çıkıyor, son
sütun hiç gelmiyor.

**Beklenen çıktı:**

```
[79.1, 78.9, 1.0]
[1.0, 1.0]
```
