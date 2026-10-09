`second_largest(numbers)` fonksiyonunu yaz: listedeki **en büyükten küçük
olan en büyük değeri** döndürsün. Böyle bir değer yoksa `None` döndürsün.

**Örnekler:**

- `[4, 9, 7, 9]` → `7` (iki tane 9 var; ikinci en büyük **farklı** değer 7)
- `[5, 5]` → `None` (en büyükten küçük değer yok)
- `[3]` ve `[]` → `None`

**Kurallar:** `sorted()`, `.sort()` ve `max()` kullanma. Listeyi **bir kez**
gezmen yeterli.

**Fikir:** Döngü boyunca iki değer tut: `first` (şimdiye kadarki en büyük)
ve `second` (ondan küçük olanların en büyüğü). İkisini de `None` ile başlat.
Yeni bir sayı `first`'ten büyükse eski `first` `second` olur.

**Beklenen çıktı:**

```
7
None
-5
```
