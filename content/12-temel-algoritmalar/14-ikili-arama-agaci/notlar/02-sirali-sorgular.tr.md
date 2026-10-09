BST'yi sözlükten ayıran şey sıra. Sözlüğün cevaplayamadığı iki soru:

## Aralık sorgusu: 4 ile 10 arasındakiler

Inorder gezinmenin budanmış hâli: aralığın dışında kalan alt ağaçlara hiç
girilmez.

```python
def in_range(node, lo, hi, out):
    if node is None:
        return out
    if lo < node.value:                # solda aralığa düşen olabilir
        in_range(node.left, lo, hi, out)
    if lo <= node.value <= hi:
        out.append(node.value)
    if node.value < hi:                # sağda aralığa düşen olabilir
        in_range(node.right, lo, hi, out)
    return out

print(in_range(root, 4, 10, []))
```

```text
[4, 6, 7, 8, 10]
```

`root` dersteki ilk ağaç (`8, 3, 10, 1, 6, 14, 4, 7, 13`). `1`, `13` ve `14`'e
hiç uğranmadı. Maliyet `O(h + k)`: `k` bulunan değer sayısı.

## Taban (floor): x'ten büyük olmayan en büyük değer

```python
def floor(node, x):
    best = None
    while node:
        if node.value == x:
            return x
        if node.value < x:             # aday; daha büyüğü sağda olabilir
            best = node.value
            node = node.right
        else:
            node = node.left
    return best

print(floor(root, 5), floor(root, 12), floor(root, 0))
```

```text
4 10 None
```

`0`'dan küçük değer olmadığı için `None`. Fiyat aralıkları, "bu tarihten
önceki son kayıt" gibi sorular hep bu.

## Aynı işler sıralı listeyle

Değerler pek değişmiyorsa sıralı liste ve `bisect` aynı soruları cevaplar:

```python
import bisect

items = [1, 3, 4, 6, 7, 8, 10, 13, 14]
bisect.insort(items, 5)                     # sırayı bozmadan ekle
print(items, bisect.bisect_left(items, 7))  # 7'nin yeri
```

```text
[1, 3, 4, 5, 6, 7, 8, 10, 13, 14] 5
```

`bisect_left(items, lo)` ile `bisect_right(items, hi)` arasındaki dilim, aralık
sorgusunun cevabı.
