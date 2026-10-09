`radix_sort(items)` fonksiyonunu yaz: negatif olmayan tam sayılardan oluşan
listeyi basamak basamak (birler, onlar, yüzler…) 10 kovayla sıralasın.

1. Boş liste boş döner.
2. `place = 1` ile başla; `max(items) // place > 0` olduğu sürece tur at.
3. Her turda 10 boş kova kur; her sayıyı `(x // place) % 10` kovasına ekle.
4. Kovaları 0'dan 9'a sırayla topla; `place *= 10`.

`sorted` ve `.sort()` kullanma.

**Beklenen çıktı:**

```
[2, 24, 45, 66, 75, 90, 170, 802]
[1, 3, 5, 5]
```
