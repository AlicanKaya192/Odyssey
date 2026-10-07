The model is prepared at startup (`ml["model"]`).

**What to do:**

1. A `Flower` model: `sepal_length`, `sepal_width`, `petal_length`,
   `petal_width`; each greater than 0, at most 10.
2. `POST /predict` → `{"species": ...}`. Build the row in this order:
   `[[sepal_length, sepal_width, petal_length, petal_width]]`.

- `5.1, 3.5, 1.4, 0.2` → `setosa`
- `5.9, 3.0, 4.2, 1.5` → `versicolor`
- `6.7, 3.0, 5.2, 2.3` → `virginica`
- a missing measurement or `-1` → `422`
