Aynı değişikliği iki kitaba iki farklı yöntemle uygula ve farkı gözünle gör.

**Yapman gerekenler:**

1. `change_and_read(method, book_id)` fonksiyonunu yaz: `requests.request`
   ile verilen yöntemle (`"PUT"` ya da `"PATCH"`) `/books/<book_id>`
   adresine `{"title": "Changed", "price": 9.0}` gövdesini göndersin, sonra
   kitabı `GET` ile okuyup **sözlük olarak** döndürsün.
2. 15 numaralı kitaba `PATCH`, 14 numaralı kitaba `PUT` uygula. Her biri
   için yöntemi, başlığı, fiyatı, yılı ve etiketleri yazdır.

`requests.request("PATCH", url, ...)` yöntemi metin olarak alan genel
fonksiyon; `requests.patch(url, ...)` ile aynı işi yapıyor.

**Beklenen çıktı:**

```
PATCH Changed 9.0 1968 ['fantasy']
PUT Changed 9.0 0 []
```
