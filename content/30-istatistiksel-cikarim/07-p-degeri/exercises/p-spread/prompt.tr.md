Gerçek %10 farkı olan aynı deney (300'er kişi) 2000 kez tekrarlandı. Tek
deneyin p'sini yazdırmak yerine alt alta şunları yaz: `p < 0.05` olanların
payı (güç, 3 basamak) ve p'nin 10., 50. ve 90. yüzdelikleri
(`np.round(np.percentile(p, [10, 50, 90]), 3).tolist()`).

**Beklenen çıktı:**

```text
0.41
[0.002, 0.082, 0.574]
```
