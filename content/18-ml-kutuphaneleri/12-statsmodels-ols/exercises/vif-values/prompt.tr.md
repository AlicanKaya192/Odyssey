`vif_values(columns)` verilen sütunların VIF değerlerini (1 basamak) sırayla
döndürsün. Kodlarda veriye çoğu zaman önce `sm.add_constant` ile sabit sütun
eklenir (eski statsmodels sürümlerinde VIF ancak böyle doğru çıkıyordu; 0.15
sonucu kendisi düzeltiyor). Sabit eklenince sıra kayar: 0. sütun `const`,
verilen sütunlar 1'den başlar. Başlangıç kodu sabiti ekliyor ama sırayı 0'dan
başlatıyor; ilk değer `const`'unki çıkıyor, son sütun hiç gelmiyor.

**Beklenen çıktı:**

```
[79.1, 78.9, 1.0]
[1.0, 1.0]
```
