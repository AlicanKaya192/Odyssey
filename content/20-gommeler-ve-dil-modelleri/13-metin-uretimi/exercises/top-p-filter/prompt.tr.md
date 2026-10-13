`top_p_filter(probs, p)` kelimeleri büyükten küçüğe dolaşıp olasılıklarını
toplasın; toplam `p`'ye ulaştığı (ya da geçtiği) ilk kelimede dursun. Tutulan
kelimelerin olasılıklarını toplamları 1 olacak şekilde ölçeklesin (3
basamak).

**Beklenen çıktı:**

```
0.75 order=0.625 parcel=0.375
0.4 order=1.0
1.0 order=0.5 parcel=0.3 box=0.15 app=0.05
```
