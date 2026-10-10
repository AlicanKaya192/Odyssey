`add_fractions(items)` `"1/3"` gibi kesir metinlerini topluyor ama `float`
kullandığı için sonuç kesir değil `0.3333333333333333` gibi yaklaşık bir
ondalık çıkıyor. `Fraction` ile yeniden yaz; sonucu sade kesir metni olarak
(`"1/2"`) döndürsün. Toplam tam sayıysa `Fraction` onu `"1"` diye yazar.

**Beklenen çıktı:**

```
1/2
7/8
```
