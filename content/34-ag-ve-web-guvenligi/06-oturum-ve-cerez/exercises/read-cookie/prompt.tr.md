Çerez `deger.etiket` biçiminde; etiket, değerin `key` ile HMAC-SHA256
onaltılık özeti. `read_cookie(cookie, key)` **son** noktadan bölsün,
etiketi yeniden hesaplayıp `hmac.compare_digest` ile karşılaştırsın;
tutarsa değeri, tutmazsa ya da nokta yoksa `None` döndürsün. `key`
metindir (`encode()`).

**Beklenen çıktı:**

```
user=ada
None
None
```
