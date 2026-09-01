Bazı fonksiyonlar aradıklarını bulamaz. Bunu belirtimde söylemek,
kullanan kişiye kontrol etmesi gerektiğini haber veriyor.

**Yapman gerekenler:**

1. `find_grade` adında bir fonksiyon yaz:
   - Parametresi `name`, bir metin.
   - İçinde `{"Ada": 90, "Alan": 70}` sözlüğü var.
   - İsim sözlükte varsa notunu döndür, yoksa `None` döndür.
   - Dönüş belirtimi **hem tam sayı hem `None`** ihtimalini anlatmalı.

2. `["Ada", "Grace"]` listesindeki her isim için fonksiyonu çağır:
   - Sonuç `None` ise `isim not found` yazdır.
   - Değilse `isim not` yazdır.

**Beklenen çıktı:**

```
Ada 90
Grace not found
```

Dikkat: `print(person, grade)` yazdığında Python araya kendiliğinden boşluk
koyuyor.

> "Ya tam sayı ya hiçbir şey" dikey çizgiyle yazılıyor. `None` kontrolü
> `is None` ile yapılır, `== None` ile değil.
