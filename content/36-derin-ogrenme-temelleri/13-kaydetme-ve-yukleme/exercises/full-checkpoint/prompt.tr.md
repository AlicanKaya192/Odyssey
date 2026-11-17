`resume_matches` 6 turluk eğitimi 3 + 3 tur olarak, arada kontrol noktası
kaydedip sürdürüyor; ama sonuç kesintisiz eğitimle aynı çıkmıyor (`False`),
çünkü Adam'ın durumu kaydedilmiyor. Kontrol noktasına optimizer'ın
`state_dict()`'ini de koy ve sürdürürken yükle. Sonuç `True` olmalı.

**Beklenen çıktı:**

```
True
```
