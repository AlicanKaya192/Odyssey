Tersini yap: bir isteğin bilgilerinden curl komutu üret. Bir hatayı birine
anlatırken ya da belgeye örnek koyarken çok işe yarar.

**Yapman gerekenler:** `to_curl(method, url, headers)` fonksiyonunu yaz.
Komut şu parçaların boşlukla birleşimi olsun:

1. `curl`
2. Yöntem `GET` değilse `-X` ve yöntem.
3. Adres.
4. Her başlık için `-H "Ad: değer"` (çift tırnakla, sözlükteki sırayla).

Sonra `samples` listesindeki her istek için komutu yazdır.

**Beklenen çıktı:**

```
curl https://api.example.com/books
curl https://api.example.com/stats -H "X-API-Key: abc"
curl -X DELETE https://api.example.com/books/7 -H "Authorization: Bearer abc"
```
