Dört kitap eklemeye çalışacaksın; üçü kurallara uymuyor. Sunucunun ne
dediğini okuyup yazdıracaksın.

**Yapman gerekenler:** `books` listesindeki her kitap için:

1. `POST /books` ile gönder (`json=`, `headers=AUTH`).
2. Kod `201` ise `created` ve `Location`'ı, değilse durum kodunu ve
   gövdedeki `detail`'i yazdır.

**Beklenen çıktı:**

```
422 title must be a non-empty string
422 price must be a positive number
422 author_id does not exist
created /books/24
```
