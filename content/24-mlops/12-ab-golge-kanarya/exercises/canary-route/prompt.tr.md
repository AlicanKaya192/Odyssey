Dersteki yönlendirmeyi yazan `route(customer_id, percent)` fonksiyonunu yaz:

- `customer_id` bir metin (`"C06-00001"` gibi).
- Kova: `zlib.crc32(customer_id.encode()) % 100`.
- Kova `percent`'ten küçükse `"new"`, değilse `"old"` döndür.

**Beklenen çıktı:**

```
39
old new
True
```
