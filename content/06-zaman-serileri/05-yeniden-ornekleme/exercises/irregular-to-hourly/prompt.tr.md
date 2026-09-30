`machine_log.csv` bir makinenin sıcaklık kayıtları. Sensör düzenli
aralıkla değil, rastgele aralıklarla kayıt göndermiş ve bir süre hiç
göndermemiş.

**Yapman gerekenler:**

1. Dosyayı `index_col="time"` ve `parse_dates=True` ile oku; `temp_c`
   sütununu `temp` serisine al.
2. Art arda iki kayıt arasındaki en uzun aralığı yazdır:
   `temp.index.to_series().diff().max()`.
3. Saatlik ortalamaya çevir (`resample("h").mean()`); saat sayısını ve boş
   (`NaN`) saat sayısını aynı satıra yazdır.
4. Boş saatleri `"%m-%d %H:%M"` biçiminde liste olarak yazdır.
5. 7 Mayıs 04:00 için `resample("h").sum()` ve `resample("h").mean()`
   sonuçlarını aynı satıra yazdır.
6. Saatlik seriyi `interpolate()` ile doldur ve 7 Mayıs 05:00 değerini iki
   ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
0 days 05:42:44
72 4
['05-07 03:00', '05-07 04:00', '05-07 05:00', '05-07 06:00']
0.0 nan
57.64
```

Beşinci satır tuzağı gösteriyor: hiç kayıt olmayan saatin toplamı 0.0,
ortalaması `nan`. Makine sıfır derecede değildi; ölçüm yoktu. Son satırdaki
değer ise bir ölçüm değil, iki uç arasına çekilmiş düz çizginin üstündeki bir
tahmin.
