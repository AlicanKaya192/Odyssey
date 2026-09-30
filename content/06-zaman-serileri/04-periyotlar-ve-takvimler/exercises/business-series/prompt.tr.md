`stock_price.csv` bir hissenin kapanış fiyatı. Borsa hafta sonu kapalı;
bu seride hafta sonu satırı **olmaması** normal.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `close` sütununu `close` serisine al.
2. pandas'ın tahmin ettiği frekansı yazdır (`pd.infer_freq`).
3. Seriyi yanlış takvime (`asfreq("D")`) ve doğru takvime (`asfreq("B")`)
   oturtunca oluşan `NaN` sayılarını aynı satıra yazdır.
4. Mart 2024'teki işlem günü sayısını yazdır.
5. 2024'ün ilk üç ayı için **ay sonu kapanışını** yazdır: aya göre grupla
   (`to_period("M")`) ve `last()` al; her ayı `ay kapanış` biçiminde bir
   satıra.

**Beklenen çıktı:**

```
B
312 0
21
2024-01 157.19
2024-02 139.47
2024-03 166.33
```

Fiyat bir toplam değil, anlık değer. Aylığa çevirirken toplanmıyor; ayın
**son** değeri alınıyor. Hafta sonlarını "eksik" sayıp doldursaydın 312 tane
hiç var olmamış fiyat uydurmuş olurdun.
