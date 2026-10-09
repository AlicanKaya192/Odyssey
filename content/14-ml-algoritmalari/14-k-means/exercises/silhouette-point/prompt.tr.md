`silhouette_point(X, labels, i)` fonksiyonunu yaz. `a`: `i`. noktanın
kendi kümesindeki **diğer** noktalara ortalama (kare değil, gerçek) uzaklığı;
`b`: diğer her kümeye ortalama uzaklıklarından en küçüğü.
`s = (b − a) / max(a, b)`, `round(..., 3)`. Her kümede en az iki nokta var.

**Beklenen çıktı:**

```
0.868
0.849
```
