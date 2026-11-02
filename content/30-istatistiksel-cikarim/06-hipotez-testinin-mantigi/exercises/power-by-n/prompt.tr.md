Açılışlar gerçekten 40 ms yavaşlasaydı, 20 ve 80 ölçümlük testler bunu ne
sıklıkla yakalardı? Her `n` için eski sürelerden 3000 tane `n`'lik örneklem
çek, **her değere 40 ekle**, `old.mean()`'e karşı `ttest_1samp` (`axis=1`)
uygula ve `p < 0.05` olanların payını `n` ile birlikte yazdır (3 basamak).
Başlangıç kodu 40'ı eklemeyi unutmuş: yanlış alarm oranını ölçüyor.

**Beklenen çıktı:**

```text
20 0.294
80 0.846
```
