Parquet istatistikleriyle yalnızca Aralık siparişlerini içerebilecek satır
gruplarını oku.

**Yapman gerekenler:**

1. `orders.parquet` hazır: 400 000 sipariş, zamana göre sıralı, 50 000'lik
   satır grupları.
2. Her satır grubunda `order_time` sütununun istatistiğine bak
   (`pf.metadata.row_group(i).column(col).statistics`); en büyük değeri
   `"2024-12"`'den küçük olmayan grupları seç.
3. Yalnızca o grupları `read_row_group` ile okuyup Aralık siparişlerini
   (`order_time` `"2024-12"` ile başlayan) say.
4. Okunan grup sayısını ve toplam grup sayısını aynı satıra, sonra Aralık
   sayısını yazdır.
5. Dosyanın tamamından sayılan Aralık sayısıyla aynı mı, yazdır.

**Beklenen çıktı:**

```
1 8
33784
True
```
