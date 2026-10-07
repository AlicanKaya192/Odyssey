Bazı kitap numaraları sunucuda yok. Durum koduna bakmadan gövdeyi okuyan kod
bu numaralarda düşer.

**Yapman gerekenler:**

1. `get_title(book_id)` fonksiyonunu yaz: `/books/<book_id>` adresine istek
   göndersin; durum kodu `200` ise kitabın başlığını, değilse `None`
   döndürsün.
2. `ids` listesindeki her numara için numarayı ve sonucu yazdır.

**Beklenen çıktı:**

```
4 -> Solaris
99 -> None
12 -> Animal Farm
0 -> None
```
