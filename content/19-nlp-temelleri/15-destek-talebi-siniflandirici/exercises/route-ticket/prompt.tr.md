`route(text)` bir sözlük döndürsün:

- `"category"`: hazır `pipe`'ın tahmini (düz metin, `str`)
- `"orders"`: metindeki sipariş numaraları (`ORD-` + beş rakam, kelime
  sınırlı)
- `"urgent"`: küçük harfe çevrilmiş metinde `"urgent"` geçiyor mu

**Beklenen çıktı:**

```
category shipping
orders ['ORD-55120']
urgent True
```
