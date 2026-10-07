Şehir başına ortalama birim fiyatı CSV'yi parça parça okuyarak doğru
hesapla ve yanlış yolla farkını gör.

**Yapman gerekenler:**

1. `orders.csv` (300 000 satır) hazır. `chunksize=70_000` ile oku.
2. Her parçada şehir başına `unit_price` toplamını ve sayısını
   `totals`, `counts` sözlüklerinde biriktir.
3. Karşılaştırma için her parçada şehir başına ortalamayı da
   `chunk_means` sözlüğünde (şehir → liste) topla.
4. Doğru ortalamaları (`totals / counts`) büyükten küçüğe sıralayıp ilk üç
   şehri ve ortalamayı (iki ondalık) yazdır.
5. `Istanbul` için doğru ortalamayı ve parça ortalamalarının ortalamasını
   (ikisi de dört ondalık) aynı satıra yazdır.

**Beklenen çıktı:**

```
Izmir 748.67
Bursa 745.81
Konya 738.41
736.2608 736.8614
```
