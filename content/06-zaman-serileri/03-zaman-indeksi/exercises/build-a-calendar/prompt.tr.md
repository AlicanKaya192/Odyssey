`pd.date_range` ile dört farklı takvim üret. Bu alıştırmada dosya yok.

**Yapman gerekenler:**

1. Mart 2024'teki iş günlerini (`freq="B"`) üret ve sayısını yazdır.
2. 2024'ün ilk altı ayının ay sonlarını (`freq="ME"`) üret ve `"%m-%d"`
   biçiminde liste olarak yazdır.
3. 9 Mart 2024 06:00'dan başlayan, 8 saat aralıklı 4 vardiya başlangıcını
   (`periods=4`, `freq="8h"`) üret ve `"%d %H:%M"` biçiminde liste olarak
   yazdır.
4. Mart 2024'teki pazartesileri (`freq="W-MON"`) üret; sayısını ve ilkini
   (`"%Y-%m-%d"`) aynı satıra yazdır.

**Beklenen çıktı:**

```
21
['01-31', '02-29', '03-31', '04-30', '05-31', '06-30']
['09 06:00', '09 14:00', '09 22:00', '10 06:00']
4 2024-03-04
```

İkinci satırda Şubat `02-29`: `date_range` artık yılı biliyor. Üçüncü satırda
son vardiya ertesi güne geçti. Ay sonu için `"M"` yazsaydın hata alırdın;
yeni pandas'ta doğrusu `"ME"`.
