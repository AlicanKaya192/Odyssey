Her olay `[zaman, ip, kullanici, sonuc]`; sonuç `"fail"` ya da `"ok"`.
`compromised(events, threshold)` aynı `(ip, kullanici)` çiftinden en az
`threshold` başarısızlığın **ardından** gelen her başarılı giriş için
`"<zaman> <kullanici> <ip>"` satırını, olay sırasıyla döndürsün. Başarılı
girişten sonra o çiftin sayacı sıfırlanır.

**Beklenen çıktı:**

```
10:04 bob 203.0.113.9
```
