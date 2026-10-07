Adresleri ezberlemeden, kök adresin verdiği bağlantılarla gezin.

**Yapman gerekenler:**

1. `GET /` ile kök adresi oku; `links` sözlüğünü yazdır.
2. `links["books"]` bağlantısını izleyip toplam kitap sayısını (`meta.total`)
   yazdır.
3. `links["authors"]` bağlantısını izleyip yazar sayısını yazdır.

Adresleri kodunda yazma (`"/books"` gibi); bağlantılardan al.

**Beklenen çıktı:**

```
{'books': '/books', 'authors': '/authors', 'stats': '/stats'}
books: 23
authors: 8
```
