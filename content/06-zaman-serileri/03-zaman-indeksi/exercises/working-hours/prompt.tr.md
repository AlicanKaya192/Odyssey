`energy_hourly.csv` bir bölgenin saatlik elektrik tüketimi (MW).
Tüketim günün saatine ne kadar bağlı?

**Yapman gerekenler:**

1. Dosyayı `index_col="timestamp"` ve `parse_dates=True` ile oku;
   `load_mw` sütununu `load` serisine al.
2. 15 Mart 2024'te kaç kayıt olduğunu yazdır.
3. Gündüz (`between_time("08:00", "18:00")`) ve gece
   (`between_time("22:00", "06:00")`) ortalamalarını bir ondalığa yuvarlayıp
   aynı satıra yazdır.
4. Gündüz ortalamasının gece ortalamasına oranını iki ondalığa yuvarlayıp
   yazdır.
5. Her günün saat 18:00'indeki (`at_time`) ortalama tüketimi bir ondalığa
   yuvarlayıp yazdır.

**Beklenen çıktı:**

```
24
1038.1 768.4
1.35
871.2
```

Gündüz tüketimi gecenin üçte bir fazlası. Bu, her gün tekrar eden 24 adımlık
bir mevsimsellik: saatlik veride tahmin yaparken en güçlü ipucu.
