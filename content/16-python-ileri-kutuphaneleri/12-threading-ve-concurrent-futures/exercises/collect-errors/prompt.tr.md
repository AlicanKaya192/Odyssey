`run_all(values)` her değeri `pool.submit(check, value)` ile havuza versin ve
sonuçları **girdi sırasıyla** bir listede döndürsün. `check` eksi sayıda
`ValueError` fırlatıyor; o değerin yerine listeye `"error"` metni yazılsın.
Başlangıç kodu hatayı yakalamadığı için tamamen düşüyor.

**Beklenen çıktı:**

```
[10, 'error', 30]
[]
```
