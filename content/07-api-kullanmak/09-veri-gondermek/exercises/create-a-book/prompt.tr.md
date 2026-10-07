Le Guin'in bir kitabını kütüphaneye ekle.

**Yapman gerekenler:**

1. `new_book` sözlüğünü `POST /books` ile, `json=` ve `headers=AUTH`
   kullanarak gönder.
2. Durum kodunu, `Location` başlığını, sunucunun verdiği numarayı ve
   yanıttaki yazar adını yazdır.

**Beklenen çıktı:**

```
status: 201
location: /books/24
id: 24
author: Le Guin
```
