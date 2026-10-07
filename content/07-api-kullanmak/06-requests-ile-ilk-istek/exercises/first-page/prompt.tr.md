`GET /books` kitap listesini döndürüyor. Yanıt bir zarf: kitaplar `data`'da,
sayfa bilgisi `meta`'da (Bölüm 05).

**Yapman gerekenler:**

1. `http://api.odyssey.test/books` adresine istek gönder.
2. `titles` adlı bir listeye bu sayfadaki kitapların başlıklarını topla.
3. Toplam kitap sayısını, bu sayfadaki kitap sayısını ve başlıkları
   aşağıdaki biçimde yazdır.

**Beklenen çıktı:**

```
total: 23
on this page: 5
Emma
Dune
Ulysses
Solaris
Persuasion
```
