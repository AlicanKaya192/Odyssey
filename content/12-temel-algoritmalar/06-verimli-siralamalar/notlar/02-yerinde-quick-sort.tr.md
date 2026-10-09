Dersteki quick sort her katta yeni listeler kuruyordu. Gerçek uygulamalar
ayırmayı listenin **içinde**, elemanları yer değiştirerek yapar. En kolay
anlaşılan yöntem **Lomuto bölmesi**:

```python
import random

def partition(items, lo, hi):
    pivot_index = random.randint(lo, hi)              # rastgele pivot
    items[pivot_index], items[hi] = items[hi], items[pivot_index]
    pivot = items[hi]
    boundary = lo                                      # solu: pivottan küçükler
    for i in range(lo, hi):
        if items[i] < pivot:
            items[i], items[boundary] = items[boundary], items[i]
            boundary += 1
    items[boundary], items[hi] = items[hi], items[boundary]
    return boundary                                    # pivotun son yeri

def quick_sort_in_place(items, lo=0, hi=None):
    if hi is None:
        hi = len(items) - 1
    if lo < hi:
        p = partition(items, lo, hi)
        quick_sort_in_place(items, lo, p - 1)
        quick_sort_in_place(items, p + 1, hi)

data = [9, 4, 7, 1, 8, 2]
quick_sort_in_place(data)
print(data)            # [1, 2, 4, 7, 8, 9]
```

## Bölme nasıl çalışıyor?

`boundary` bir çizgi: solundaki her eleman pivottan **küçük**. `i` listeyi
soldan sağa geziyor; pivottan küçük bir eleman bulunca onu çizginin hemen
sağına alıp çizgiyi bir ilerletiyor. Gezinti bitince pivot (sonda bekliyordu)
çizginin yerine konuyor: solunda küçükler, sağında büyük ya da eşitler.

Ek liste yok; yalnızca özyineleme yığını kullanılıyor (ortalama `O(log n)`).
Rastgele pivot sayesinde sıralı girdi de hızlı ve derinlik sınırına
takılmıyor.

## Kararlılık

Uzak yer değiştirmeler eşit elemanların sırasını bozabilir: yerinde quick
sort kararlı değildir. Kararlılık gerekiyorsa merge sort ya da Python'un
`sorted`'ı.
