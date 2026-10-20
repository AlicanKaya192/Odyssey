Sunma ve izleme bölümlerini birleştiren `prediction_record(customer_id, score, version, threshold)` fonksiyonunu yaz. Bir sözlük döndürsün:

- `"id"`: müşteri kimliği, `"version"`: model sürümü.
- `"score"`: skor, üç basamağa yuvarlanmış.
- `"decision"`: skor en az `threshold` ise `"offer"`, değilse `"no offer"`.

**Beklenen çıktı:**

```
C06-00001 3
0.426 offer
no offer
```
