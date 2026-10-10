`square_all(numbers, n_workers)` fonksiyonunu yaz:

- Bir `tasks` ve bir `results` kuyruğu (`queue.Queue`) kur.
- `n_workers` iş parçacığı başlat; her işçi `tasks`'tan alsın, `STOP`
  görünce çıksın, değilse sayının karesini `results`'a koysun.
- Sayıları kuyruğa koy, sonra her işçi için bir `STOP` koy, işçileri `join`
  et.
- Kareleri **sıralı** liste olarak döndür.

**Beklenen çıktı:**

```
[1, 4, 9]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
