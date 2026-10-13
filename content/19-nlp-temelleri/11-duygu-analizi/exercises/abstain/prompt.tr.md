Sözlük bazen çok zayıf bir puanla karar veriyor. `coverage_accuracy(margin)`
yalnızca `abs(puan) > margin` olan yorumlara karar versin (`scores` hazır):
puan > 0 ise `"positive"`, değilse `"negative"`. `[kapsama, doğruluk]`
döndürsün, ikisi de 3 basamak: kapsama karar verilen yorumların oranı,
doğruluk bunların içinde doğru tahminin oranı.

**Beklenen çıktı:**

```
0 [0.777, 0.881]
1 [0.436, 0.979]
2 [0.182, 0.997]
```
