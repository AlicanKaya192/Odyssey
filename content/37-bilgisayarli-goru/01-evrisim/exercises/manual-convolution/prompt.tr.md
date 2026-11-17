`convolve(img, kernel)` iki iç içe listeyi (resim ve çekirdek) alıp dolgusuz,
adımı 1 olan evrişimi (derste olduğu gibi, çekirdeği çevirmeden) yalnızca
döngülerle hesaplasın. Çıktı `(H - kh + 1) x (W - kw + 1)` iç içe liste.
PyTorch kullanma.

**Beklenen çıktı:**

```
[[-5, -5, -5], [-5, -5, -5]]
[[6, 9], [18, 21], [30, 33]]
```
