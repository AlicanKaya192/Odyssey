Yanında bir `media` klasörü var (alt klasörüyle birlikte üç dosya).

`fits(folder, free)` fonksiyonunu yaz: klasördeki bütün dosyaların toplam
boyutunu bayt olarak bulsun (`rglob`, `stat().st_size`) ve
`(toplam, toplam <= free)` demetini döndürsün. Gerçekte `free` değeri
`shutil.disk_usage(...).free`'den gelir.

**Beklenen çıktı:**

```
(18, True)
(18, False)
```
