`vigenere` ve `ioc` (harf listesi alır) hazır. `secret` yalnızca küçük
harflerden oluşur.

`key_length(secret, max_len, threshold)` 1'den `max_len`'e her uzunluk
`L` için metni `L` sütuna bölsün (`secret[i::L]`), sütunların ortalama
IoC'sini hesaplasın ve ortalaması `threshold`'a eşit ya da büyük olan
**ilk** (en küçük) `L`'yi döndürsün. Hiçbiri yoksa `0`.

**Beklenen çıktı:**

```
5
3
1
```
