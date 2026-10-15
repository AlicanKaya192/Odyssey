Bir Dockerfile'ın adımları `[komut, baktığı dosyalar, saniye]` listesi. `total_seconds(steps, builds)` fonksiyonunu yaz: `builds` art arda yapılan derlemelerin listesi, her biri o derlemede değişen dosyaların listesi. Önbellek derlemeler arasında korunuyor. Bütün derlemelerin toplam süresini döndür.

- **İlk derlemede** önbellek boş: bütün adımlar çalışır.
- Sonrakilerde: bir adımın baktığı dosyalardan biri değiştiyse **o adım ve sonraki her adım** çalışır; öncekiler önbellekten gelir (0 saniye).

İki kesişen küme: `set(a) & set(b)` boş değilse ortak öğe var.

**Beklenen çıktı:**

```
good order: 132
bad order: 310
```
