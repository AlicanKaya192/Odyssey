`forest_size(level)` ormanı `compress=level` ile kaydetsin ve dosya boyunu KB
olarak (`// 1024`) döndürsün. Başlangıç kodu `level`'ı kullanmıyor.

Sıkıştırılmış dosyanın boyu Python'un kullandığı sıkıştırma kütüphanesine
göre birkaç KB değişiyor (Windows'taki Python zlib-ng, macOS'taki zlib
kullanıyor). Bu yüzden alttaki satırlar sıkıştırmasız boyu birebir,
sıkıştırılmışı ise üçte birinden küçük mü diye denetliyor.

**Beklenen çıktı:**

```
626
True
```
