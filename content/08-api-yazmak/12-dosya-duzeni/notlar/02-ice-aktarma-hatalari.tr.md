Dosyalara bölünce çıkan hatalar ve anlamları.

## Döngüsel içe aktarma

`main.py` `models`'i, `models.py` de `main`'i içe aktarıyorsa:

```text
ImportError: cannot import name 'Book' from 'models'
(consider renaming '...models.py' if it has the same name as a library ...)
```

Python 3.14'ün mesajı (ölçtük). Sona eklenen "adını değiştir" önerisi bu
durumda **yanıltıcı**: asıl sebep, `models` henüz yarıdayken (`Book`
tanımlanmadan) `main`'in onu istemesi. Çözüm içe aktarmayı tek yöne
çevirmek: `models.py` hiçbir proje dosyasını içe aktarmasın.

## `ModuleNotFoundError: No module named 'routers'`

- `routers/__init__.py` yok, ya da
- program proje klasörünün dışından çalıştırılıyor.

## `ImportError: cannot import name 'router' from 'routers.books'`

`routers/books.py` içinde değişkenin adı `router` değil (örneğin
`books_router`). `main.py`'deki ad ile dosyadaki ad aynı olmalı.

## Uç nokta görünmüyor (`404`)

- `app.include_router(...)` satırı unutuldu.
- Önek iki kez yazıldı: router'da `prefix="/books"` varken uç nokta da
  `@router.get("/books")` → adres `/books/books`.

## Aynı adın iki dosyada olması

`routers/books.py` ve `models.py` ikisi de `Book` tanımlarsa hangisinin
kullanıldığı içe aktarmaya bağlı kalır. Modeller **yalnızca**
`models.py`'de.
