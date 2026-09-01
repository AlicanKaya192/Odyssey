Bu alıştırmada `print` fonksiyonunun ayrıntılarını bir arada
kullanacaksın: ayırıcı değiştirme, satır sonunu kapatma ve hesap yaptırma.

**Yapman gerekenler:**

1. Üç satır yazdır. Her satırda ürün adı ve fiyatı **nokta ile** ayrılsın —
   aradaki boşluklar aynen aşağıdaki gibi olsun:

```
apple.3
bread.5
milk.4
```

   Bunun için `print` fonksiyonunun `sep` ayarını kullan.

2. Sonra bir satırda `total:` yaz, **alt satıra geçmeden**, hemen ardından
   üç fiyatın toplamını yazdır. Bunun için `end` ayarını kullan.

**Beklenen çıktı:**

```
apple.3
bread.5
milk.4
total:12
```

Dikkat: dördüncü satırda `total:` ile `12` arasında **boşluk yok**.
Toplamı elle `12` yazma, Python'a hesaplatır.

> `print("a", "b", sep=".")` iki değeri nokta ile ayırıyor.
> `print("x", end="")` yazdıktan sonra alt satıra geçmiyor.
