Kayıttaki deneyler bir liste: her deneyde `"run"` (numara), `"params"` ve `"metrics"` sözlükleri var. `best_run(runs, metric)` fonksiyonunu yaz:

- `metrics` içinde `metric` ölçümü en yüksek olan deneyin **numarasını** döndür.
- O ölçümü olmayan deneyleri atla.
- Eşitlikte önce gelen (listede daha önce duran) kazansın.
- Hiçbir deneyde o ölçüm yoksa `None` döndür.

**Beklenen çıktı:**

```
2
3
None
```
