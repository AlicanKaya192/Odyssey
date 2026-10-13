`threshold_report(inside, outside, loss)` eşiği gerçek taleplerin (`inside`)
puanlarından seçsin: sıralanmış listenin `int(loss · uzunluk)` sıradaki
değeri. Sonra `[eşik, eşiğe eşit ya da büyük gerçek talep oranı, eşiğin
altında kalan ilgisiz metin oranı]` döndürsün (oranlar 3 basamak).

**Beklenen çıktı:**

```
[0.3, 0.9, 0.6]
[0.4, 0.7, 0.8]
```
