700 siparişin günü (`make_weekday_orders(n=700, seed=161)`). Gün sayımlarını
Pazartesi'den Pazar'a liste olarak yazdır, sonra eşit dağılıma karşı
`stats.chisquare` ile sına: χ² (2 basamak) ve p (4 basamak). Başlangıç
kodu teste **oranları** veriyor (`normalize=True`); ki-kare sayım ister.

**Beklenen çıktı:**

```text
[82, 93, 80, 85, 104, 141, 115]
29.2 0.0001
```
