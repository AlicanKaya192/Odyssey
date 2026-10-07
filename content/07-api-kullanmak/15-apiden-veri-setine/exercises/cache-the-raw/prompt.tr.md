Ham yanıtı diske yaz; ikinci çağrıda API'ye hiç gitme.

**Yapman gerekenler:**

1. `load_books(session)` fonksiyonunu yaz: `books_raw.json` dosyası varsa
   onu okuyup döndürsün ve `from cache` yazdırsın; yoksa `fetch_all` ile
   çeksin, dosyaya yazsın, `from api` yazdırsın ve döndürsün.
2. `load_books`'u **iki kez** çağır; her seferinde gelen kitap sayısını
   yazdır.

`get_json` ve `fetch_all` hazır.

**Beklenen çıktı:**

```
from api
books: 23
from cache
books: 23
```

Kontrol, iki çağrı boyunca toplam yalnızca 2 istek atıldığına bakıyor.
