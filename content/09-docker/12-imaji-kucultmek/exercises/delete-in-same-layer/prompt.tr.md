Bu imaj 30 MB'lık geçici bir dosya oluşturuyor, özetini alıyor ve dosyayı
siliyor; ama üç ayrı `RUN` kullandığı için dosya ilk katmanda kalıyor ve
imaj ~73 MB.

**Yapman gereken:** üç `RUN`'ı `&&` ile **tek** `RUN`'da birleştir (uzun
satırı `\` ile bölebilirsin). Odyssey imajın **20 MB'tan küçük** olduğuna
bakacak.

**Beklenen çıktı:**

```
checksum ready
9
```
