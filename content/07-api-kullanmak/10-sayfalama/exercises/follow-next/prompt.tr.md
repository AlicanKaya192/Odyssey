Klasik etiketli kitapları 4'erli sayfalarla topla; sayfa numarası hesaplama,
sunucunun verdiği `next` bağlantısını izle.

**Yapman gerekenler:**

1. İlk adres: `BASE + "/books?tag=classic&per_page=4"`.
2. `while url:` döngüsünde iste, `data`'yı `classics` listesine ekle;
   `links.next` varsa `url = BASE + next`, yoksa `None`.
3. Kaç sayfa gezdiğini, kaç kitap topladığını ve her sayfada izlenen
   `next` adreslerini yazdır.

**Beklenen çıktı:**

```
next: /books?tag=classic&per_page=4&page=2
next: /books?tag=classic&per_page=4&page=3
pages: 3
classics: 12
```

`next` adresinde `tag` ve `per_page` parametrelerinin korunduğuna bak.
