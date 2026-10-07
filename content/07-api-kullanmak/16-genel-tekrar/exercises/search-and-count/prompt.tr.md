Bölüm 01, 06 ve 07'nin tekrarı: parametreli bir arama, giden adres ve sonuç.

**Yapman gerekenler:**

1. `/books`'tan **1960 ve sonrasında** yayımlanmış **bilimkurgu** kitaplarını
   iste, yıla göre **eskiden yeniye** sırala, sayfa boyu 20 olsun. Hepsini
   `params=` ile ver.
2. Giden adresi, toplam sayıyı ve her kitabı `yıl başlık` biçiminde yazdır.

**Beklenen çıktı:**

```
http://api.odyssey.test/books?tag=scifi&year_min=1960&sort=year&per_page=20
total: 8
1961 Solaris
1965 Dune
1965 The Cyberiad
1969 Dune Messiah
1969 The Left Hand of Darkness
1971 The Lathe of Heaven
1974 The Dispossessed
1986 Fiasco
```
