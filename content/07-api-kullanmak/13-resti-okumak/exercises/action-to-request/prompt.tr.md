REST'in sözleşmesini bir fonksiyona yaz: bir iş adı ve isteğe bağlı bir kimlik
verildiğinde doğru yöntemi ve adresi döndürsün.

**Yapman gerekenler:** `to_request(action, book_id)` fonksiyonu
`(yöntem, adres)` **demeti** döndürsün:

| `action` | Yöntem | Adres |
|---|---|---|
| `"list"` | `GET` | `/books` |
| `"read"` | `GET` | `/books/<id>` |
| `"create"` | `POST` | `/books` |
| `"replace"` | `PUT` | `/books/<id>` |
| `"change"` | `PATCH` | `/books/<id>` |
| `"remove"` | `DELETE` | `/books/<id>` |

`list` ve `create` için `book_id` `None` gelir. Sonra `jobs` listesindeki her
iş için yöntemi ve adresi yazdır.

**Beklenen çıktı:**

```
list -> GET /books
read -> GET /books/42
create -> POST /books
change -> PATCH /books/7
remove -> DELETE /books/3
replace -> PUT /books/9
```
