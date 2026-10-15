`critical_path(jobs)` fonksiyonunu yaz. `jobs` bir sözlük: iş adı → `[dakika, bağlı olduğu işler]`. Bir iş, bağlı olduğu işlerin en geç bitenini bekler.

`[toplam süre, yol]` döndür:

- Toplam süre: en geç biten işin bitiş dakikası.
- Yol: o işten geriye, her adımda bağlı olduklarının **en geç biteni** seçilerek, baştan sona sıralı iş adları.
- Eşitlikte sözlükte (ya da `needs` listesinde) önce gelen seçilir; `max(..., key=...)` zaten öyle yapar.

**Beklenen çıktı:**

```
[6, ['lint', 'test', 'build']]
[8, ['docs', 'build']]
```
