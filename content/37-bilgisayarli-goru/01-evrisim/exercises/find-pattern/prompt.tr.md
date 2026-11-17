`find_pattern(img, pattern)` deseni çekirdek olarak kullanıp `F.conv2d`
(dolgusuz) ile resimde en güçlü tepkinin yerini bulsun ve çıktıdaki
`[satır, sütun]`'u döndürsün (desenin sol üst köşesinin resimdeki yeri).
`argmax` düz sıra numarası verir; onu satır ve sütuna çevir.

**Beklenen çıktı:**

```
[2, 3]
[3, 3]
```
