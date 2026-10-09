## Kurulum ve sorgu

```python
prefix = [0]
for x in values:
    prefix.append(prefix[-1] + x)      # len(prefix) == len(values) + 1

def range_sum(lo, hi):                 # values[lo:hi], hi dahil değil
    return prefix[hi] - prefix[lo]
```

| | Maliyet |
|---|---|
| Kurmak | `O(n)` zaman, `O(n)` bellek |
| Bir aralık sorusu | `O(1)` |
| Veri değişirse | baştan kurmak `O(n)` (sık değişiyorsa başka yapı gerekir) |

## Sınır hataları

- Başa `0` koymazsan `values[0:hi]` için özel durum yazman gerekir.
- `hi` **dahil değil** (Python dilimleri gibi). "lo'dan hi'ye dahil"
  isteniyorsa `prefix[hi + 1] - prefix[lo]`.
- Boş aralık (`lo == hi`) toplamı 0 verir; doğru.

## İki boyut: tablo toplamları

Bir ızgarada (görüntü, ısı haritası, satış tablosu) dikdörtgen toplamları
için `P[r][c]`, sol üst köşeden `(r, c)`'ye kadar olan toplam olsun:

```python
def build_2d(grid):
    rows, cols = len(grid), len(grid[0])
    P = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
    return P

def rect_sum(P, r1, c1, r2, c2):       # satır r1..r2-1, sütun c1..c2-1
    return P[r2][c2] - P[r1][c2] - P[r2][c1] + P[r1][c1]

grid = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
P = build_2d(grid)
print(rect_sum(P, 1, 1, 3, 3))         # 5 + 6 + 8 + 9 = 28
```

Son satırdaki `+ P[r1][c1]`, iki kez çıkarılan sol üst köşeyi geri ekliyor.

## Aynı fikrin akrabaları

- **Önek en büyüğü:** `best[i] = max(best[i-1], values[i])`: "şu güne
  kadarki en yüksek fiyat".
- **Önek çarpımı:** oranların birikimi (getiri hesapları).
- **Hareketli toplam:** `prefix[i] - prefix[i - k]`; kayan pencerenin önek
  toplamıyla yazılmış hâli.
