Bölümün üç aracını birden kullanıyoruz.

Şu **üç koşulu birden** sağlayan ürünleri getir:

- kategorisi `Aksesuar` ya da `Ekran`,
- fiyatı 200 ile 2000 arasında (iki uç dahil),
- `tedarikci_kod` sütunu **boş değil**.

Sütunlar: `ad`, `kategori`, `fiyat`. Pahalıdan ucuza sırala.

```
ad         kategori  fiyat
---------  --------  -------
Mikrofon   Aksesuar  1320.00
Webcam     Aksesuar  1150.00
...
```

Sonuç dört satır olmalı. Beş bulduysan büyük ihtimalle son koşulu
atlamışsındır: fiyatı ve kategorisi uyan ama tedarikçisi kayıtlı olmayan
bir ürün var.
