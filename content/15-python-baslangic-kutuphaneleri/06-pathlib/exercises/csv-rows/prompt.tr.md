Klasörünün yanında hazır bir `shop` klasörü var:

- `shop/README.txt`
- `shop/data/sales.csv`, `stock.csv`
- `shop/data/old/sales-2025.csv`
- `shop/src/app.py`

`csv_rows(folder)` fonksiyonunu yaz: klasördeki ve alt klasörlerindeki her
`.csv` dosyası için başlık satırı hariç kaç veri satırı olduğunu sözlük olarak
döndürsün. Anahtar, dosyanın `folder`'a göre göreli yolu, `/` ile
(`rglob`, `relative_to`, `as_posix`).

**Beklenen çıktı:**

```
data/old/sales-2025.csv 4
data/sales.csv 3
data/stock.csv 2
```
