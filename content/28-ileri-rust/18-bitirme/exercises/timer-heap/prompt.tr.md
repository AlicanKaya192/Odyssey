`Entry` için sırayı yaz: En yakın süre `BinaryHeap`'in üstünde olsun (`Ord` ters). `Sleep` future'ı: Süre dolduysa `Ready`, dolmadıysa yığına `Entry` koy, `notify_one` çağır, `Pending` döndür.

**Beklenen çıktı:**

```text
[2, 3, 1]
```
