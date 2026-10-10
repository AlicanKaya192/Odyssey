## Seçim

| Yazım | Ne verir | Görünüm / kopya |
|---|---|---|
| `m[i, j]` | tek eleman | — |
| `m[i]`, `m[:, j]` | satır, sütun | görünüm |
| `m[1:, ::2]` | dilim | görünüm |
| `m[[0, 2]]` | satır listesi | kopya |
| `m[[0, 2], [1, 3]]` | (0,1) ve (2,3) **çiftleri** | kopya |
| `m[np.ix_([0, 2], [1, 3])]` | alt matris | kopya |
| `m[m > 5]` | maske, düz dizi | kopya |
| `m[..., 0]` | son eksende 0 (Ellipsis) | görünüm |

## Atama

| Yazım | Sonuç |
|---|---|
| `m[m > 5] = 0` | `m` değişir |
| `m[[0, 1], 0] = 0` | `m` değişir |
| `m[m > 5][0] = 0` | `m` değişmez (kopyaya yazıldı) |

## Koşul ve konum

| Yazım | Ne yapar |
|---|---|
| `(a > 0) & (a < 5)`, <code>&#124;</code>, `~` | maskeleri birleştir (parantez şart) |
| `np.where(k, a, b)` | koşula göre değer |
| `np.where(k)[0]`, `np.nonzero(a)[0]` | konumlar |
| `np.argsort(a)`, `a.argmax(axis=...)` | sıralama sırası, en büyüğün yeri |
| `np.unique(a, return_counts=True)` | benzersizler ve sayıları |
| `np.isin(a, liste)` | listede var mı |
| `np.clip(a, alt, üst)` | sınırla |
| `a[:, np.newaxis]` | yeni eksen |
