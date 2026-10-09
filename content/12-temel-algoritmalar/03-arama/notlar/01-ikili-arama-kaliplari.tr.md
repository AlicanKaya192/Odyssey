İkili aramanın üç sık kalıbı. Üçünde de bölge her turda yarıya iner:
`O(log n)`.

## 1. Tam eşleşme

```python
def binary_search(items, target):
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Değişmez (invariant):** hedef listede varsa her zaman `lo..hi` aralığında.
Bölge boşalınca (`lo > hi`) hedef yok.

## 2. Hedefe eşit ya da büyük ilk yer (alt sınır)

```python
def lower_bound(items, target):
    lo, hi = 0, len(items)          # hi = len: "hiçbiri değil" cevabı da olabilir
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

`bisect.bisect_left` ile aynı sonucu verir. Dikkat: bu kalıpta `hi`
aralığa **dahil değil** (yarı açık aralık), bu yüzden koşul `lo < hi` ve
`hi = mid` doğru. Kalıpları **karıştırma**: birinin `hi`'sini öbürünün
koşuluyla kullanmak dersteki gibi eleman kaçırır ya da sonsuz döngüye
sokar.

## 3. Cevap üzerinde arama

"Koşul `k`'de doğruysa daha büyük `k`'lerde de doğru" (ya da tersi) olan bir
koşulda, koşulun değiştiği yeri bulmak:

```python
def first_true(lo, hi, condition):
    # condition(lo..hi) önce False, sonra hep True; ilk True'yu döndürür.
    while lo < hi:
        mid = (lo + hi) // 2
        if condition(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Örnekler: "En az kaç kutu yeter?", "En büyük `k` ile `k * k <= n`",
"Hangi sürümde hata başladı?" (git'in `bisect` komutu tam olarak bu).

## Test listesi

İkili arama yazınca şunları **mutlaka** dene:

- Boş liste, tek elemanlı liste
- Listedeki **her** değer (ilk, son, ortadakiler)
- Listede olmayan değerler: en küçükten küçük, en büyükten büyük, iki
  elemanın arası
- Tekrar eden değerler (ilk/son geçiş isteniyorsa)

## `mid` hesabı

Python'da tam sayılar taşmaz; `(lo + hi) // 2` güvenli. Java, C gibi
dillerde `lo + hi` çok büyük olunca taşabildiği için `lo + (hi - lo) // 2`
yazılır. Python'da ikisi de aynı sonucu verir.
