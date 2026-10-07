Belgelerdeki örnekler curl komutu. Bir komutu parçalarına ayırıp isteğin
bilgilerini çıkaran bir fonksiyon yazacaksın.

**Yapman gerekenler:** `parse_curl(command)` fonksiyonunu yaz. Komutu
`shlex.split` ile böl, `curl`'den sonraki parçaları sırayla oku:

- `-X` → sonraki parça yöntem,
- `-H` → sonraki parça bir başlık (`"Ad: değer"`, ilk `": "`'dan böl),
- `-d` → sonraki parça gövde,
- bunların dışında kalan parça → adres.

Yöntem verilmemişse: gövde varsa `"POST"`, yoksa `"GET"`. Şunu döndür:
`{"method": ..., "url": ..., "headers": {...}, "data": ... ya da None}`.

Sonra `commands` listesindeki her komut için yöntemi, adresi, başlık sayısını
ve gövdeyi yazdır.

**Beklenen çıktı:**

```
GET http://api.odyssey.test/books/1 0 None
GET http://api.odyssey.test/stats 1 None
POST http://api.odyssey.test/books 2 {"title": "Kindred", "price": 11.5}
```
