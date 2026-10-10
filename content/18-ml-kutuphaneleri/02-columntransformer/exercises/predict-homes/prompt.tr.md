`predict_homes(rows, prices, new_rows)` ham `[size, city, id]` tablosundan fiyat
tahmin eden **tek** bir nesne kursun: `make_pipeline(hazırlık,
LinearRegression())`. Hazırlık: `size` medyanla doldurulsun, `city`
`OneHotEncoder(handle_unknown="ignore")`, `id` atılsın. `rows` ve `prices`
ile eğitip `new_rows` için tahminleri 1 basamağa yuvarlı liste döndürsün. Yeni
satırlarda eksik boyut ya da görülmemiş şehir olabilir.

**Beklenen çıktı:**

```
[1966.7, 2055.6]
```
