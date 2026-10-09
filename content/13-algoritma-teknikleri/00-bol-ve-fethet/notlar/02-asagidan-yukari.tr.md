Böl ve fethet genelde yukarıdan aşağı, özyinelemeyle yazılır: büyük problemi
böl, böl, böl. Aynı işi **aşağıdan yukarı** da yapabilirsin: en küçük
parçalardan başla, ikişer ikişer birleştirerek yukarı çık. Özyineleme yok,
çağrı yığını yok.

## Aşağıdan yukarı merge sort

```python
def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]

def merge_sort_bottom_up(values):
    runs = [[x] for x in values]          # her eleman tek başına sıralı
    while len(runs) > 1:
        runs = [merge(runs[k], runs[k + 1]) if k + 1 < len(runs) else runs[k]
                for k in range(0, len(runs), 2)]
        print(runs)
    return runs[0] if runs else []

merge_sort_bottom_up([5, 2, 8, 1, 9, 3])
```

```text
[[2, 5], [1, 8], [3, 9]]
[[1, 2, 5, 8], [3, 9]]
[[1, 2, 3, 5, 8, 9]]
```

Her tur bir seviye: altı tek elemanlı parça → üç ikili → iki parça → bir
liste. Tur sayısı `⌈log₂ n⌉`, her tur `n` iş: yine `O(n log n)`.

## Ne zaman tercih edilir?

- **Özyineleme derinliği sorun olacaksa.** Yarıya bölen merge sort'un
  derinliği yalnızca `log n` (bir milyon eleman için 20), ama her
  böl-fethet bu kadar sığ değil.
- **Veri zaten parça parça geliyorsa.** Python'un Timsort'u listedeki hazır
  sıralı parçaları (koşuları) bulup aşağıdan yukarı birleştirir; sıralıya
  yakın veride bu yüzden çok hızlıdır.
- **Belleğe sığmayan veride.** Dosyayı parça parça sıralayıp diske yazmak,
  sonra parçaları birleştirmek (dış sıralama) aşağıdan yukarı düşünmenin
  aynısı; Temel Algoritmalar modülündeki `heapq.merge` bu son adımı yapıyordu.
