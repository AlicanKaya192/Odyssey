`hash_buckets(text, buckets)` fonksiyonunu yaz: metni küçük harfe çevirip
boşluklardan böl; her kelimenin sütunu `zlib.crc32(kelime.encode()) % buckets`.
Her sütuna düşen kelime sayısını `buckets` uzunlukta bir liste olarak
döndürsün.

**Beklenen çıktı:**

```
[3, 0, 1, 0, 0, 0, 2, 0]
[0, 0, 0, 3]
```
