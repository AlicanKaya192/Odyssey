Bağlantı koptu ve beş isteğin yanıtı gelmedi. Hangilerini düşünmeden
yeniden gönderebilirsin?

Tekrarlanabilir yöntemler: `GET`, `HEAD`, `OPTIONS`, `PUT`, `DELETE`. `POST`
ve `PATCH` değil.

**Yapman gerekenler:**

1. `can_retry(method)` fonksiyonunu yaz: yöntem tekrarlanabilirse `True`,
   değilse `False` döndürsün. Yöntem küçük harfle de gelebilir (`"patch"`);
   karşılaştırmadan önce büyük harfe çevir.
2. `failed` listesindeki her istek için, yeniden gönderilebiliyorsa
   `retry`, değilse `ask first` yaz; ardından yöntemi (büyük harfle) ve
   adresi yaz.

**Beklenen çıktı:**

```
retry GET /books
ask first POST /orders
retry DELETE /books/7
ask first PATCH /books/7
retry PUT /books/7
```
