1000 kişilik örneklemden (`random_state=32`) alışveriş yapanların payını
tahmin et. Alt alta üç sayı yazdır: örneklemdeki pay (4 basamak), standart
hatası `sqrt(p_hat * (1 - p_hat) / n)` (4 basamak) ve tahminin gerçek
paydan kaç standart hata uzakta olduğu, `(p_hat - true_p) / se` (2
basamak).

**Beklenen çıktı:**

```text
0.12
0.0103
0.57
```
