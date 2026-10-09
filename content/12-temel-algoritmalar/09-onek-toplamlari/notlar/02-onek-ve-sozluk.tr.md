"Önek toplamı + sözlük" kalıbının üç sık türevi. Üçünde de liste bir kez
geziliyor: `O(n)`.

## 1. Toplamı k olan en uzun parça

Sayıyı değil, önek toplamının **ilk görüldüğü indeksi** sakla: en uzun parça
için en soldaki başlangıç gerekir.

```python
def longest_sum_k(values, k):
    first_index = {0: -1}          # boş önek, -1. konumda
    total = 0
    best = 0
    for i, x in enumerate(values):
        total += x
        if total - k in first_index:
            best = max(best, i - first_index[total - k])
        if total not in first_index:   # yalnızca ilk görülüşü tut
            first_index[total] = i
    return best

print(longest_sum_k([1, -1, 5, -2, 3], 3))   # 4  (1, -1, 5, -2)
```

## 2. Eşit sayıda 0 ve 1 içeren en uzun parça

Her `0`'ı `-1` say; "eşit sayıda" demek "toplamı 0" demek. Böylece soru
1. türeve dönüşür (`k = 0`).

```python
def longest_balanced(bits):
    return longest_sum_k([1 if b == 1 else -1 for b in bits], 0)

print(longest_balanced([0, 1, 0, 0, 1, 1, 0]))   # 6
```

## 3. Toplamı k'ye bölünen parçaları saymak

İki önek toplamının farkı `k`'ye bölünüyorsa, ikisinin `k`'ye bölümünden
kalanlar eşittir. Sözlükte kalanları say:

```python
def count_divisible(values, k):
    seen = {0: 1}
    total = 0
    count = 0
    for x in values:
        total += x
        r = total % k                  # Python'da negatif sayıda da 0..k-1
        count += seen.get(r, 0)
        seen[r] = seen.get(r, 0) + 1
    return count

print(count_divisible([4, 5, 0, -2, -3, 1], 5))   # 7
```

## Ne zaman bu kalıp?

Soru **"ardışık parça"** ve **"toplam/ortalama/denge"** içeriyorsa ve sayılar
negatif olabiliyorsa, önce bu kalıbı dene. Sayılar hep pozitifse kayan pencere
de yeter ve sözlük gerektirmez.
