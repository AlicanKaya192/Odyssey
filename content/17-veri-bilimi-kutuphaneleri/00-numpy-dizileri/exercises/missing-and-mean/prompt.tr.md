`missing_and_mean(values)` listede `None` olabilir. Listeyi
`np.array(values, dtype=float)` ile ondalık diziye çevir (`None` → `nan`),
eksik sayısını (`np.isnan(...).sum()`) ve eksikler hariç ortalamayı
(`np.nanmean`, 2 basamağa yuvarlı) `[eksik, ortalama]` olarak döndür.

**Beklenen çıktı:**

```
[1, 4.0]
[0, 2.0]
```
