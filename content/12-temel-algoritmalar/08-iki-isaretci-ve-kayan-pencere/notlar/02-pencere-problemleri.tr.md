Kayan pencere veri işinde çok sık çıkar; çoğunun hazır bir aracı da vardır.

## Hareketli ortalama

```python
def moving_average(values, k):
    result = []
    total = 0
    for i, value in enumerate(values):
        total += value
        if i >= k:
            total -= values[i - k]          # pencereden çıkan
        if i >= k - 1:
            result.append(total / k)
    return result

print(moving_average([2, 4, 6, 8, 10], 3))   # [4.0, 6.0, 8.0]
```

pandas'ta aynı iş `series.rolling(3).mean()`; Zaman Serileri patikasında
bolca kullanıldı. İçinde bu kaydırma fikri çalışır.

## Toplamı en az `target` olan en kısa parça (negatif olmayan sayılar)

```python
def shortest_at_least(values, target):
    start = 0
    total = 0
    best = None
    for end, value in enumerate(values):
        total += value
        while total >= target:                  # şart sağlandı: küçültmeyi dene
            length = end - start + 1
            if best is None or length < best:
                best = length
            total -= values[start]
            start += 1
    return best

print(shortest_at_least([2, 3, 1, 2, 4, 3], 7))   # 2  (4 + 3)
```

## Son `k` eleman: `deque(maxlen=k)`

Bir akışta yalnızca son `k` olayı tutmak gerekiyorsa `collections.deque`'in
`maxlen` ayarı pencereyi kendiliğinden kaydırır:

```python
from collections import deque

last_three = deque(maxlen=3)
for event in [5, 1, 7, 3, 9]:
    last_three.append(event)
print(list(last_three))          # [7, 3, 9]
```

Büyük Veri patikasının akan veri bölümündeki zaman pencereleri de aynı
fikrin zamana göre hâli.
