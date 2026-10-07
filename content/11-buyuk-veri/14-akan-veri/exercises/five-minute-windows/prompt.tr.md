İlk 2000 ödemeyi beş dakikalık (300 saniye) sabit pencerelere böl; her
pencere kapanınca sonucunu yazdır.

**Yapman gerekenler:**

1. Pencerenin başlangıcı: `event["ts"] // 300 * 300`.
2. Yalnızca açık pencerenin başlangıcını, ödeme sayısını ve toplam tutarını
   tut.
3. Yeni bir pencerenin ilk ödemesi gelince eskisini yazdır:
   `closed başlangıç sayı toplam` (toplam iki ondalık).
4. Akış bitince açık kalan son pencereyi `open başlangıç sayı toplam`
   biçiminde yazdır.

**Beklenen çıktı:**

```
closed 0 207 23060.11
closed 300 212 23432.8
closed 600 215 25068.68
closed 900 208 26918.22
closed 1200 212 24829.54
closed 1500 215 26446.96
closed 1800 225 26956.03
closed 2100 213 25240.26
closed 2400 197 26540.65
open 2700 96 10348.27
```
