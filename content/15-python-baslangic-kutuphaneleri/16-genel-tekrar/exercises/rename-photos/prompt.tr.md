Yanında bir `photos` klasörü var. Telefonun verdiği `IMG_20260315_101500.jpg`
gibi adları `2026-03-15_10-15-00.jpg` biçimine çevir.

`rename_photos(folder)` fonksiyonunu yaz: adı `IMG_(\d{8}_\d{6})\.jpg`
kalıbına **tam** uyan her dosyanın tarihini `datetime.strptime(...,
"%Y%m%d_%H%M%S")` ile okusun, `strftime("%Y-%m-%d_%H-%M-%S")` ile yeni adı
kursun ve `rename` etsin. Uymayanlara dokunmasın. Sonunda klasördeki adları
sıralı döndürsün.

**Beklenen çıktı:**

```
2026-03-15_10-15-00.jpg
2026-03-16_08-30-12.jpg
IMG_bad.jpg
notes.txt
```
