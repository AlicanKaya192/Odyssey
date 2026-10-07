Süzme, sıralama ve sınırlamayı tek istekte birleştir: `classic` etiketli
kitaplardan en ucuz üçü.

**Yapman gerekenler:**

1. `/books` adresine üç parametreyle istek gönder: `tag`, `sort`, `per_page`.
   (Sıralama küçükten büyüğe: `sort=price`.)
2. Gelen kitapların başlığını ve fiyatını yazdır.
3. Son satırda `meta.total`'ı yazdır: klasik etiketli kitapların toplamı.

**Beklenen çıktı:**

```
Animal Farm 6.9
Dubliners 7.8
Persuasion 8.75
classics in total: 12
```
