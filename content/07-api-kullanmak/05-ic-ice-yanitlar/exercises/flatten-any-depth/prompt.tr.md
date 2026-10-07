İç içelik iki, üç kat olabilir. Her katı elle yazmak yerine kendini çağıran
bir fonksiyon yazacaksın.

**Yapman gerekenler:**

1. `flatten(obj, prefix="")` fonksiyonunu yaz. `obj` bir sözlük. Döndürdüğü
   düz sözlükte:
   - değer sözlük değilse anahtar `prefix + key` adıyla olduğu gibi girer,
   - değer sözlükse fonksiyon **kendini** o sözlük için
     `prefix + key + "_"` önekiyle çağırır ve sonucu ekler (`update`).
   Listeler olduğu gibi kalır.
2. `record`'u düzleştirip her anahtarı ve değerini `ad = değer` biçiminde
   yazdır.

**Beklenen çıktı:**

```
id = 7
title = Emma
author_name = Austen
author_address_city = Bath
author_address_country = UK
tags = ['classic', 'novel']
```
