`sales_messy.csv` bir mağazanın 2024 satışı (`date`, `sales`), sistemden
çıktığı hâliyle: satırlar karışık, bazı günler iki parça hâlinde yazılmış,
bazı günler hiç yok.

**Yapman gerekenler:**

1. Dosyayı `parse_dates=["date"]` ile oku.
2. Satır sayısını, farklı gün sayısını ve `sales` sütunundaki `NaN` sayısını
   aynı satıra yazdır.
3. İki kez geçen tarihleri `"%m-%d"` biçiminde, sıralı bir liste olarak
   yazdır.
4. Aynı günün parçalarını topla (`groupby("date")["sales"].sum()`), sırala ve
   `asfreq("D")` ile her güne bir satır aç. Sonucun uzunluğunu ve `NaN`
   sayısını aynı satıra yazdır.
5. Eksik günleri `"%m-%d"` biçiminde liste olarak yazdır.
6. Boşlukların uzunluklarını liste olarak yazdır
   (`(missing != missing.shift()).cumsum()` sayacı).

**Beklenen çıktı:**

```
362 358 0
['03-05', '06-18', '09-09', '11-30']
366 8
['02-10', '02-11', '04-23', '07-15', '07-16', '07-17', '10-29', '12-25']
[2, 1, 3, 1, 1]
```

Dosyada tek bir `NaN` yoktu, ama 8 gün eksikti. Düzenli indeks kurulmadan
eksik veri sayılamaz. Boşluklar 1 ile 3 gün arasında: doldurulabilecek kadar
kısa.
