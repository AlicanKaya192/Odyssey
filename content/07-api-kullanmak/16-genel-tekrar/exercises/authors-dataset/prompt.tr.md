Bölüm 05, 13 ve 15'in tekrarı: iç içe kaynaklardan bir veri seti kur.

**Yapman gerekenler:**

1. `GET /authors` ile yazarları al.
2. Her yazar için `GET /authors/<id>/books` ile kitaplarını iste; kitap
   sayısını, en eski ve en yeni yılı ve ortalama fiyatı (iki ondalık) içeren
   bir satır kur: `name`, `country`, `books`, `first`, `last`, `avg_price`.
3. Satırları `authors.csv`'ye yaz.
4. Dosyayı okuyup içeriğini yazdır.

**Beklenen çıktı:**

```
name,country,books,first,last,avg_price
Austen,UK,4,1811,1817,10.19
Herbert,US,2,1965,1969,10.45
Joyce,IE,2,1914,1922,11.4
Lem,PL,3,1961,1986,12.2
Orwell,UK,3,1938,1949,8.83
Le Guin,US,4,1968,1974,10.09
Tolstoy,RU,2,1869,1878,16.1
Woolf,UK,3,1925,1928,9.23
```
