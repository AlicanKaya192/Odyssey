Başlangıç kodunda dersteki `predict` kuralı hazır. `compare(n)` ilk `n` yorumda
iki doğruluğu 3 basamağa yuvarlayıp `[kural, taban_cizgisi]` listesi olarak
döndürsün:

- kural: `predict(text)` etiketi kaç yorumda doğru bildi, oranı
- taban çizgisi: **en sık etiketin** payı (hep onu söyleyen tahminin doğruluğu)

En sık etiketi elle yazma; `Counter(...).most_common(1)` ile bul.

**Beklenen çıktı:**

```
[0.449, 0.659]
```
