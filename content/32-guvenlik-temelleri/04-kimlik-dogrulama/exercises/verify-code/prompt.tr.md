`hotp` hazır. `verify_code(secret, code, unix_time)` kullanıcının yazdığı
kodu denetlesin:

- Şu anki sayaç `unix_time // 30`.
- Saat kaymasına karşı sayaç `- 1`, sayacın kendisi ve `+ 1` için üretilen
  üç kodu kabul et.
- Karşılaştırmayı `==` ile değil `hmac.compare_digest(a, b)` ile yap:
  `==` ilk farklı karakterde durur ve geçen süre ipucu verebilir;
  `compare_digest` her zaman bütün metni karşılaştırır.

Eşleşen varsa `True`, yoksa `False` döndür.

**Beklenen çıktı:**

```
True
True
False
False
```
