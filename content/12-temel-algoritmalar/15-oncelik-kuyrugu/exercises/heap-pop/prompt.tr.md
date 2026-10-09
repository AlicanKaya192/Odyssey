`push` (yukarı kaydırma) hazır. `pop(heap)` fonksiyonunu **`heapq` kullanmadan**
yaz: en küçüğü çıkarıp döndürsün, kalan listeyi yine heap bıraksın.

1. Son elemanı listeden çıkar (`heap.pop()`). Liste boş kaldıysa onu döndür.
2. Kökü sakla, yerine o son elemanı yaz.
3. `i = 0`'dan başla: `2i + 1` ve `2i + 2` çocuklarından (varsa) **küçük**
   olanı bul. O, `heap[i]`'den küçükse yer değiştir ve oraya in; değilse dur.
4. Saklanan kökü döndür.

`pop_all(values)` hepsini `push` ile ekleyip `pop` ile sırayla çıkarıyor.

**Beklenen çıktı:**

```
[1, 2, 3, 5, 8, 9]
[1, 4, 4, 7]
```
