`png_size(width, height, dpi)` `figsize=(width, height)` boyutunda bir şekil
açsın, içine bir çizgi çizsin, `out.png` olarak **`dpi=dpi`** ile kaydetsin
(`bbox_inches` verme). Kaydedilen resmi `matplotlib.image.imread` ile okuyup
`[genişlik, yükseklik]` piksel döndürsün. Şekli kapat. Not: `imread(...).shape`
`(yükseklik, genişlik, kanal)` verir.

**Beklenen çıktı:**

```
[400, 300]
[750, 300]
```
