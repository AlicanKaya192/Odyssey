`stock_price.csv` bir hissenin kapanış fiyatı. Fiyatın ne kadar oynak
olduğunu ve uzun dönem ortalamasının üstünde mi altında mı seyrettiğini ölç.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `close` serisini ve günlük getiriyi
   (`pct_change()`) hesapla.
2. 20 günlük hareketli oynaklığı yıllıklandırılmış yüzde olarak hesapla:
   `r.rolling(20).std() * (252 ** 0.5) * 100`.
3. Oynaklığın ortalamasını bir ondalığa yuvarlayıp yazdır.
4. En yüksek oynaklığın tarihini (`"%Y-%m-%d"`) ve değerini (bir ondalık)
   aynı satıra yazdır; sonra aynısını en düşük oynaklık için yazdır.
5. 100 günlük hareketli ortalamayı hesapla (`close.rolling(100).mean()`).
   2024'te fiyatın bu ortalamanın **üstünde** kapandığı gün sayısını ve
   2024'teki toplam işlem günü sayısını aynı satıra yazdır.

**Beklenen çıktı:**

```
27.0
2023-03-02 39.8
2023-10-18 18.5
157 262
```

Oynaklık sabit bir sayı değil: en sakin dönemle en çalkantılı dönem arasında
iki kattan fazla fark var. Risk ölçerken tek bir ortalama oynaklık yerine o
günkü hareketli değere bakılmasının sebebi bu.
