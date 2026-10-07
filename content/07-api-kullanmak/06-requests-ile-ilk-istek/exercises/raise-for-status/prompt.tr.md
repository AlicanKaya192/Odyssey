Dört adrese istek atacaksın; ikisi var, ikisi yok. Her istekten sonra `if`
yazmak yerine `raise_for_status()` kullan.

**Yapman gerekenler:** `paths` listesindeki her adres için:

1. İsteği gönder ve hemen `raise_for_status()` çağır.
2. Hata yoksa `ok`, adres ve gövdedeki `title` ya da `name` değerini yazdır
   (kitapta `title`, yazarda `name` var; `get` ile ikisini de dene).
3. `requests.HTTPError` gelirse `failed`, adres ve durum kodunu yazdır.

**Beklenen çıktı:**

```
ok /books/5 Persuasion
failed /books/0 404
ok /authors/3 Joyce
failed /authors/42 404
```
