`readings(hours, temps, at)` `at` saatindeki sıcaklığı iki yolla tahmin etsin:
doğrusal (`np.interp`) ve aşmayan eğri (`interpolate.PchipInterpolator`).
`[doğrusal, pchip]` döndürsün (2'şer basamak).

**Beklenen çıktı:**

```
[18.5, 18.7]
[11.0, 10.31]
```
