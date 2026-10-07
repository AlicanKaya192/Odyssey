Parquet dosyasından yalnızca iki sütun okuyup şehir başına ortalama fiyatı
bul.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişlik türlü `df`'yi hazırlıyor; onu
   `orders.parquet` olarak yaz.
2. `columns=["city", "unit_price"]` ile yalnızca iki sütunu oku.
3. Okunan tablonun sütun listesini yazdır.
4. İki sütunluk okumanın ve bütün dosyanın belleğini MB olarak (bir ondalık,
   `memory_usage(deep=True)`) aynı satıra yazdır.
5. Şehir başına ortalama fiyatı bul (`groupby("city", observed=True)`), büyükten
   küçüğe sırala ve ilk üç şehri ortalamalarıyla (bir ondalık) yazdır.

**Beklenen çıktı:**

```
['city', 'unit_price']
1.7 8.2
Trabzon 744.1
Izmir 741.4
Istanbul 741.4
```

`observed=True` yalnızca veride görülen kategorileri gruplamasını söylüyor.
