Bir sunucuya gelen isteklerin zamanları (saniye, artan sırada) veriliyor.
`recent_counts(times, window)` fonksiyonunu yaz: her istek geldiğinde,
**son `window` saniye** içinde (o an dahil, `t - window`'dan büyük olanlar)
kaç istek geldiğini bir listede döndürsün.

- `recent_counts([1, 2, 5, 12, 13], 10)` → `[1, 2, 3, 2, 3]`
  (12 geldiğinde 1 ve 2 pencereden çıktı: 5 ve 12 kaldı)

Bir **kuyruk** (`deque`) tut: yeni zamanı sona ekle, pencereden çıkanları
baştan at (`popleft`). Listeyle `pop(0)` kullanma.

**Beklenen çıktı:**

```
[1, 2, 3, 2, 3]
[]
```
