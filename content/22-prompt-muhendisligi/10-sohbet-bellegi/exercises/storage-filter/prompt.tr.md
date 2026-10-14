`store_all(texts)` her metin için saklama kararı versin: hazır `SECRET`
kalıbı metinde bulunursa `"not stored"` (o metinden hiçbir şey alınmaz),
yoksa `"stored"` ve metindeki bütün sipariş numaralarını (`ORDER.findall`)
listeye ekle. Döndür: `[kararlar, sipariş numaraları]`.

**Beklenen çıktı:**

```
stored
not stored
not stored
stored
['ORD-48213', 'ORD-23345', 'ORD-55102']
```
