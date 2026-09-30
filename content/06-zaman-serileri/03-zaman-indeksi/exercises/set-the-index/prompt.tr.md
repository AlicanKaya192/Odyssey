`store_sales.csv` dosyasını tarih indeksli bir seri olarak oku ve
tarihle seçmeyi dene.

**Yapman gerekenler:**

1. Dosyayı `index_col="date"` ve `parse_dates=True` ile oku; `sales` sütununu
   `s` adlı seriye al.
2. İndeksin türünün adını yazdır: `type(s.index).__name__`.
3. 9 Mart 2024'ün satışını yazdır.
4. Mart 2024'ün toplam satışını yazdır.
5. 2024 yılının ortalama satışını bir ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
DatetimeIndex
384
8919
294.0
```

Geçen bölümde Mart toplamını iki koşul yazarak bulmuştun. Tarih indekste
olunca `"2024-03"` yazmak yetiyor.
