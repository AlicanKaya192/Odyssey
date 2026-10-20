Bir tasarım belgesinde eksik bölümleri bulan `missing_sections(doc, required)` fonksiyonunu yaz:

- `doc` bir metin; bölüm başlıkları `"## "` ile başlayan satırlar.
- Başlığın adı `"## "`'den sonrası, boşlukları kırpılmış.
- `required` listesindeki adlardan belgede başlık olarak geçmeyenleri, aynı sırayla döndür.

**Beklenen çıktı:**

```
['Model', 'Monitoring']
[]
```
