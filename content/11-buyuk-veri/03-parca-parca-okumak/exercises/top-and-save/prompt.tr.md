Parçalarla iki iş yap: en yüksek cirolu üç siparişi bul ve cirosu 20 000
TL'yi geçen siparişleri ayrı bir dosyaya yaz.

**Yapman gerekenler:**

1. 200 000 siparişlik dosyayı yaz.
2. 50 000 satırlık parçalarla oku. Her parçada `revenue = quantity *
   unit_price` sütununu ekle.
3. Her parçanın `nlargest(3, "revenue")` sonucunu bir listeye koy.
4. Aynı döngüde `revenue >= 20_000` olan satırları `large.csv` dosyasına
   **ekleyerek** yaz: ilk parçada `mode="w"` ve başlıklı, sonrakilerde
   `mode="a"` ve başlıksız, `index=False`.
5. Döngüden sonra listeyi birleştirip yeniden `nlargest(3, "revenue")` al;
   her satıra `order_id` ve ciroyu (iki ondalık) yazdır.
6. `large.csv` dosyasını oku; satır sayısını ve en küçük cirosunu (iki
   ondalık) aynı satıra yazdır.

**Beklenen çıktı:**

```
77834 37969.65
64034 37358.2
181799 35445.5
284 20058.12
```

Dosyadaki en küçük ciro 20 000'in üstünde: süzme doğru çalıştı.
