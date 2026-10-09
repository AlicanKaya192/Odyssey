`combination_sum(candidates, target)` fonksiyonunu **budamalı geri izlemeyle**
yaz: farklı pozitif tam sayılardan, her biri **en fazla bir kez** kullanılarak,
toplamı `target` olan bütün seçimleri döndürsün. Her seçim küçükten büyüğe,
seçimler de üretildiği sırayla (önce sayıları sırala).

- `[10, 1, 2, 7, 6, 5]`, `8` → `[[1, 2, 5], [1, 7], [2, 6]]`

Toplam hedefi geçtiği an `break`: sonraki sayılar daha büyük. Son satırda
1–40 arasından 30 yapan seçimler sayılıyor; `2⁴⁰` alt kümeyi budamadan gezen
çözüm hiç bitmez.

**Beklenen çıktı:**

```
[[1, 2, 5], [1, 7], [2, 6]]
296
```
