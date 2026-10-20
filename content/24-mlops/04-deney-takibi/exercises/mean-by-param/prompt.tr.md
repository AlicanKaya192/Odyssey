Bir ayarın etkisini görmek için, o ayarın her değeri için ölçümün **ortalamasını** al. `mean_by_param(runs, param, metric)` fonksiyonunu yaz:

- `params` içinde `param` olmayan deneyleri atla.
- Ayarın her değeri için `metric` ölçümlerinin ortalamasını üç basamağa yuvarla.
- `[[değer, ortalama], ...]` listesi döndür; değerler deneylerde **ilk göründükleri sırayla**.

**Beklenen çıktı:**

```
max_depth 3 0.785
max_depth 5 0.815
```
