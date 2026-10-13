`apply_temperature(probs, t)` bir kelime → olasılık sözlüğünü sıcaklıkla
yeniden ağırlıklasın: her olasılığı `p ** (1 / t)` yap, sonra toplamları 1
olacak şekilde böl. 3 basamak, kelimelerin sırası korunsun.

**Beklenen çıktı:**

```
0.5 order=0.783 parcel=0.196 box=0.022
1.0 order=0.6 parcel=0.3 box=0.1
2.0 order=0.473 parcel=0.334 box=0.193
```
