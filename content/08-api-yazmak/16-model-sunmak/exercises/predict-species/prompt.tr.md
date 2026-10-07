Model açılışta hazırlanıyor (`ml["model"]`).

**Yapman gerekenler:**

1. `Flower` modeli: `sepal_length`, `sepal_width`, `petal_length`,
   `petal_width`; her biri 0'dan büyük, en fazla 10.
2. `POST /predict` → `{"species": ...}`. Satırı bu sırayla kur:
   `[[sepal_length, sepal_width, petal_length, petal_width]]`.

- `5.1, 3.5, 1.4, 0.2` → `setosa`
- `5.9, 3.0, 4.2, 1.5` → `versicolor`
- `6.7, 3.0, 5.2, 2.3` → `virginica`
- eksik ölçü ya da `-1` → `422`
