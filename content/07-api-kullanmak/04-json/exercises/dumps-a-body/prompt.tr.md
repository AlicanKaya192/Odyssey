Bir API'ye yeni kitap ekleyeceksin (`POST /books`). Gövdede gidecek veri
şimdilik bir Python sözlüğü; onu JSON metnine çevirmen gerekiyor.

**Yapman gerekenler:**

1. `json.dumps` ile `book`'u `text` adlı bir metne çevir ve yazdır.
2. Aynı sözlüğü `indent=2` ile okunur biçimde bir kez daha yazdır.

**Beklenen çıktı:**

```
{"title": "Emma", "author": "Austen", "available": true, "note": null}
{
  "title": "Emma",
  "author": "Austen",
  "available": true,
  "note": null
}
```

Çıktıda `True`'nun `true`'ya, `None`'un `null`'a dönüştüğüne ve tırnakların
çift olduğuna bak.
