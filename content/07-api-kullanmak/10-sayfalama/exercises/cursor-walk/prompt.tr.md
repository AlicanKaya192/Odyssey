`/cursor/books` imleçle sayfalıyor: yanıt `{"results": [...], "next_cursor":
...}`. İlk istekte imleç yok; sonrakilerde bir önceki yanıtın `next_cursor`
değerini `cursor` parametresiyle geri gönderiyorsun.

**Yapman gerekenler:**

1. `fetch_all()` fonksiyonunu yaz: bütün kitapları imleçle toplasın ve
   **başlıkların listesini** döndürsün. `next_cursor` `None` olunca dursun.
2. Fonksiyonu çağır; kaç kitap geldiğini, ilk ve son başlığı yazdır.

**Beklenen çıktı:**

```
books: 23
first: Emma
last: The Lathe of Heaven
```

İmleci yorumlama; olduğu gibi geri gönder.
