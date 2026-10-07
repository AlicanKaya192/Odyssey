Sense and Sensibility (7 numara) kütüphaneden çıkıyor.

**Yapman gerekenler:**

1. `DELETE /books/7` gönder; durum kodunu ve gövdenin boş olup olmadığını
   (`r.text == ""`) yazdır.
2. `GET /books/7` ile silindiğini doğrula; durum kodunu yazdır.
3. Aynı silmeyi bir kez daha gönder; durum kodunu yazdır.

**Beklenen çıktı:**

```
delete: 204 empty body: True
get after delete: 404
delete again: 404
```

İkinci silmenin kodu farklı ama sonuç aynı: kitap yok.
