Model ve `Flower` hazır; `to_row(flower)` dört ölçüyü sırayla veriyor.

**Yapman gereken:** `POST /predict/batch`, gövde bir `Flower` listesi:

- boş liste → `422` (`"Send at least one flower"`)
- 5'ten fazla → `413` (`"At most 5 flowers per request"`)
- yoksa **tek** `predict` çağrısıyla tür adlarının listesi

- `[setosa ölçüleri, virginica ölçüleri]` → `["setosa", "virginica"]`
