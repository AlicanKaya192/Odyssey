Yayın, `CHANGELOG.md`'deki sürüm bölümünü not olarak kullanacak. `release_notes(changelog, version)` fonksiyonunu yaz:

- Bölüm `## [0.4.0]` ile başlayan satırdan sonra başlar (satırın devamında tarih olabilir).
- Bir sonraki `## [` ile başlayan satırda ya da metnin sonunda biter.
- Bölümün satırlarını `"\n"` ile birleştir, baştaki ve sondaki boşlukları at (`strip`), döndür.
- Sürümün bölümü yoksa `None`.

**Beklenen çıktı:**

```
- Add kelvin conversion.
- Round results to two places.
---
- First release.
---
None
```
