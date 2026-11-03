**Diffie-Hellman + anahtar türetme.** `derive` hazır (ortak sırdan
HMAC ile 32 baytlık anahtar). `session_key(p, g, a, b)` iki tarafın
oturum anahtarını hesaplayıp `[eşit_mi, ada_anahtarı]` döndürsün. Her
taraf ortak sırrı **karşının** açık değerinden hesaplar. Başlangıç
kodunda Ada kendi açık değerini kullanıyor ve anahtarlar tutmuyor.

**Beklenen çıktı:**

```
True
32 bytes
```
