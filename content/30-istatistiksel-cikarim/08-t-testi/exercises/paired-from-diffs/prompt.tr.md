`paired_p(before, after)` eşli t-testinin p'sini `ttest_rel` kullanmadan
bulsun: farkları (`before - after`) hesapla ve onları `ttest_1samp` ile 0'a
karşı sına; p'yi 4 basamakla döndür. Başlangıç kodu `before`'u
`after`'ın ortalamasına karşı sınıyor: eşleri unutuyor.

**Beklenen çıktı:**

```text
0.0037
```
