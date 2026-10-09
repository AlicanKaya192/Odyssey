Hazır `Status` enum'unda sipariş durumları sırayla duruyor: `pending`,
`paid`, `shipped`, `delivered`. `next_status(value)` fonksiyonunu yaz: gelen
değerin **bir sonraki** durumunun değerini döndürsün; son durumdaysa `None`,
geçersiz değerse `"invalid"`. `list(Status)` sırayı verir.

**Beklenen çıktı:**

```
paid
delivered
None
invalid
```
