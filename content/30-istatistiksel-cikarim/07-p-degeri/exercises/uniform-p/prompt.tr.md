İki grubu aynı evrenden (sayfa açılış süreleri) çekip 4000 kez karşılaştır:
her satır çifti için `stats.ttest_ind(a, b, axis=1, equal_var=False)`.
Alt alta yaz: `p < 0.05` olanların payı, `p < 0.10` olanların payı (3
basamak) ve p'nin dört eşit dilime dağılımı
(`np.histogram(p, bins=4, range=(0, 1))[0].tolist()`).

**Beklenen çıktı:**

```text
0.048
0.099
[941, 968, 1019, 1072]
```
