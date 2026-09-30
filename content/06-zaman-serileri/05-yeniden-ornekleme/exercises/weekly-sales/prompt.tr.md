Günlük satışı haftalığa topla ve yarım haftalara dikkat et.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını tarih indeksli `s` serisi olarak oku.
2. Haftalık toplamı (`resample("W").sum()`) ve her haftadaki gün sayısını
   (`resample("W").count()`) hesapla.
3. İlk haftanın toplamını ve gün sayısını aynı satıra yazdır.
4. Toplam hafta sayısını ve **tam** (7 günlük) hafta sayısını aynı satıra
   yazdır.
5. Tam haftalar arasında en yüksek toplamlı haftanın etiketini
   (`"%Y-%m-%d"`) ve toplamını aynı satıra yazdır.
6. Aynısını en düşük toplamlı tam hafta için yazdır.

**Beklenen çıktı:**

```
582 2
158 156
2024-12-29 2717
2022-07-03 1357
```

İlk hafta yalnızca iki gün içeriyor. Yarım haftaları atmadan "en kötü
hafta"yı arasaydın cevap o olurdu; gerçekte ise 2022 Temmuz'unun ilk
haftası.
