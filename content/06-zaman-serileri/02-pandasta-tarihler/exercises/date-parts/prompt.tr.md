Bölüm 00'da haftanın günleri hazır bir sütundaydı. Şimdi onu tarihten
kendin üret ve mağazanın haftalık desenini ölç.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını `parse_dates=["date"]` ile oku.
2. Gün adına göre (`dt.day_name()`) ortalama satışı hesapla, büyükten küçüğe
   sırala. **İlk üç** günü `ad ortalama` biçiminde (bir ondalık) alt alta
   yazdır.
3. Hafta sonunun (`dt.dayofweek >= 5`) toplam satıştaki yüzde payını bir
   ondalığa yuvarlayıp yazdır.
4. 2024 Mart ayının toplam satışını yazdır (`dt.year` ve `dt.month`).

**Beklenen çıktı:**

```
Saturday 336.1
Sunday 296.9
Friday 278.9
34.9
8919
```

Hafta sonu takvimin 2/7'si, yani yaklaşık %28.6'sı. Satıştaki payının bundan
yüksek olması haftalık mevsimselliğin ölçüsü.
