## Kural

Şekiller **sağdan** karşılaştırılır; her eksende boylar **eşit** ya da biri
**1**. Eksik eksen başa 1 olarak eklenir.

| A | B | Sonuç |
|---|---|---|
| `(3, 4)` | `(4,)` | `(3, 4)` |
| `(3, 4)` | `(3,)` | **hata** |
| `(3, 4)` | `(3, 1)` | `(3, 4)` |
| `(3, 1)` | `(1, 4)` | `(3, 4)` |
| `(5, 1, 2)` | `(1, 3, 2)` | `(5, 3, 2)` |

## Kalıplar

| İş | Yazım |
|---|---|
| Sütun bazında merkezlemek | `X - X.mean(axis=0)` |
| Satır bazında oran | `X / X.sum(axis=1, keepdims=True)` |
| Sütun vektörü | `v[:, np.newaxis]` ya da `v.reshape(-1, 1)` |
| Her çift | `a[:, None] - b[None, :]` |
| Şekli önceden görmek | `np.broadcast_shapes(s1, s2)` |

## ufunc

| Yazım | Ne yapar |
|---|---|
| `np.add.reduce(a)` | toplam (`sum` ile aynı) |
| `np.add.accumulate(a)` | birikimli toplam |
| `np.multiply.outer(a, b)` | her çiftin çarpımı |
| `np.maximum(a, b)` | eleman eleman büyük olan |
| `f(a, out=b)` | sonucu var olan diziye yaz |
| `f(a, where=maske, out=...)` | yalnızca maskede hesapla |
| `np.vectorize(f)` | kolaylık; hız kazandırmaz |
