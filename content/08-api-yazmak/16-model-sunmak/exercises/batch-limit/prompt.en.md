The model and `Flower` are ready; `to_row(flower)` gives the four
measurements in order.

**What to do:** `POST /predict/batch`, the body is a list of `Flower`:

- empty list → `422` (`"Send at least one flower"`)
- more than 5 → `413` (`"At most 5 flowers per request"`)
- otherwise a list of species names with **one** `predict` call

- `[setosa measurements, virginica measurements]` → `["setosa", "virginica"]`
