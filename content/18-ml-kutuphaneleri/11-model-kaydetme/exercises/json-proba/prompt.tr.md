`TEXT` lojistik pipeline'ın parametrelerini JSON olarak tutuyor (`mean`,
`scale`, `coef`, `intercept`). `json_proba(rows)` yalnızca bu metinden ve
NumPy'dan olasılıkları hesaplasın (3 basamak): önce ölçekle
(`(x - mean) / scale`), sonra katsayılarla çarp, sabiti ekle, sigmoid.
Başlangıç kodu ölçeklemeyi atlıyor.

**Beklenen çıktı:**

```
[0.293, 0.817]
```
