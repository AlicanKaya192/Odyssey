İki anahtarlı gruplamanın **tablo hâlini** üreteceksin — Excel'deki pivot
tablonun aynısı.

**Yapman gerekenler:**

1. Satırlar `city`, sütunlar `grade`, hücreler not **ortalaması** olacak
   şekilde bir pivot tablo üret; adı `table` olsun.
2. `table` tablosunu yazdır.
3. Kaç hücrenin **boş** olduğunu yazdır.
4. Ankara'daki B notlularının ortalamasını yazdır.

**Beklenen çıktı:**

```
grade      A     B     C
city
Ankara  86.5  88.0   NaN
Bursa    NaN  70.0  68.0
Izmir   76.0  74.0  64.0
2
88.0
```

**`NaN` hücreler önemli:** Ankara'da C notu alan **kimse yok**. Bu, "Ankara'da
C ortalaması sıfır" demek değil — ortada hiç kayıt yok.

İkisini karıştırmamak gerekiyor. `fill_value=0` ile sıfır yazdırabilirsin
ama o zaman sonraki hesaplarda o sıfırlar gerçek ölçüm gibi davranır ve
ortalamaları aşağı çeker.
