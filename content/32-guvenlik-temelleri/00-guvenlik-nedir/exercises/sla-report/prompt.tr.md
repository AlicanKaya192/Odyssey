`sla_report(outages, days, target)` fonksiyonunu yaz:

- `outages`: o dönemdeki kesintilerin dakika cinsinden listesi,
- `days`: dönemin gün sayısı, `target`: söz verilen yüzde.

Gerçekleşen erişilebilirliği yüzde olarak hesaplayıp 3 basamağa yuvarla ve
`(yuzde, tutuldu_mu)` demeti döndür. Yuvarlanmış yüzde hedefe eşit ya da
büyükse söz tutulmuştur.

**Beklenen çıktı:**

```
(99.903, True)
(99.891, False)
(100.0, True)
```
