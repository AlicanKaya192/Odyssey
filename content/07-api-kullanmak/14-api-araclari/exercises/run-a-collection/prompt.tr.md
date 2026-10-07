Ekibin Postman'den dışa aktardığı küçük bir koleksiyon (sadeleştirilmiş) ve
bir ortam elinde. İsteklerde `{{base_url}}` ve `{{token}}` gibi yer tutucular
var.

**Yapman gerekenler:**

1. `fill(text, variables)` fonksiyonunu yaz: metindeki her `{{ad}}` yer
   tutucusunu `variables` sözlüğündeki değerle değiştirsin.
2. Koleksiyondaki her isteği sırayla çalıştır: adresi ve başlık değerlerini
   `fill` ile doldur, `requests.request` ile gönder (`body` varsa `json=`).
3. Her istek için adını ve durum kodunu yazdır.

**Beklenen çıktı:**

```
List books: 200
Who am I: 200
Add a book: 201
Missing book: 404
```
