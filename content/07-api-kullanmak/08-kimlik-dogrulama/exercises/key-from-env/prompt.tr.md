Anahtar koda yazılmaz; ortam değişkeninden okunur. Bu alıştırmada değişken
tanımlı değil, bu yüzden alıştırma sunucusunun açık anahtarı varsayılan
olarak kullanılacak.

**Yapman gerekenler:**

1. `get_key()` fonksiyonunu yaz: `LIBRARY_KEY` ortam değişkenini
   `os.environ.get` ile okusun, yoksa `"demo-key-123"` döndürsün.
2. Değişkenin tanımlı olup olmadığını yazdır (`"LIBRARY_KEY" in os.environ`).
3. `get_key()` ile aldığın anahtarla `/stats`'a istek at; kod ve kitap
   sayısını yazdır.

**Beklenen çıktı:**

```
LIBRARY_KEY defined: False
status: 200
books: 23
```

Gerçek bir projede varsayılan konmaz: anahtar yoksa program durmalı. Burada
varsayılan, alıştırmanın her bilgisayarda çalışması için.
