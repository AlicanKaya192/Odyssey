`calls` zaman sırasıyla `[t, src]` istekleri. `rate_limit(calls,
limit, window)` her istek için `True` (geçti) ya da `False` (reddedildi)
listesi döndürsün. Kural dersteki kayan pencere, ama **her kaynağın kendi
penceresi** var: bir kaynak, son `window` saniyede kabul edilmiş `limit`
isteği varsa reddedilir. Reddedilen istek pencereye girmez. Başlangıç
kodu tek bir ortak pencere kullanıyor.

**Beklenen çıktı:**

```
0 a True
1 a True
2 b True
3 a False
4 b True
12 a True
```
