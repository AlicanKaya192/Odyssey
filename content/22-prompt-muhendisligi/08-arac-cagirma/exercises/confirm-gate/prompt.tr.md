`dispatch(call, confirmed)` çağrıyı hazır `TOOLS` sözlüğüne göre
çalıştırsın: araç yoksa `{"error": "unknown tool <ad>"}`; aracın
`"confirm"` değeri `True` ve `confirmed` `False` ise
`{"pending": "needs the customer's confirmation"}`; yoksa aracın
fonksiyonunu çağrının argümanlarıyla çalıştırıp sonucunu döndür.

**Beklenen çıktı:**

```
['pending']
['cancelled', 'order_id']
['order_id', 'status']
```
