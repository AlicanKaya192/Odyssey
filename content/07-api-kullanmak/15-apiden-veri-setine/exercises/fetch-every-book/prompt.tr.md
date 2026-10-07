Hattın ilk adımı: bütün kitapları sağlam bir çekme fonksiyonuyla al.
`get_json` hazır veriliyor (zaman aşımı, 429'da bekleme, yeniden deneme).

**Yapman gerekenler:**

1. `fetch_all(session)` fonksiyonunu yaz: `get_json` ile `/books`'u
   `per_page=20` sayfalarla çeksin, `meta.pages`'e ulaşınca bütün kitapları
   döndürsün.
2. Bir `requests.Session` kur, `fetch_all`'u çağır; kitap sayısını, ilk ve
   son kitabın başlığını yazdır.

**Beklenen çıktı:**

```
books: 23
first: Emma
last: The Lathe of Heaven
```

Kontrol yalnızca 2 istek atıldığına bakıyor.
