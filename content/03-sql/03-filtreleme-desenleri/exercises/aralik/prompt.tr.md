Fiyatı **500 ile 3200 arasında** olan ürünlerin `ad` ve `fiyat` bilgisini
ucuzdan pahalıya sırala.

```
ad           fiyat
-----------  --------
Antivirus    780.00
Kulaklik     890.00
...
```

`BETWEEN` **iki ucu da dahil ediyor.** Tabloda fiyatı tam 3200 olan bir
ürün var (`Monitor`) ve sonuca giriyor — sonuç altı satır.

Beş satır bulduysan sınırı dışarıda bırakan bir yazım kullanmışsındır.
