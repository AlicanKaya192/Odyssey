Klasörünün yanında hazır bir `project` klasörü var:

- `project/main.py`, `README.txt`, `LICENSE`
- `project/data/sales.csv`, `stock.csv`
- `project/data/old/sales-2025.csv`
- `project/src/app.py`, `utils.py`
- `project/notes/todo.txt`

`find_files(folder, ext)` fonksiyonunu yaz: klasörde ve alt klasörlerinde
uzantısı `ext` olan dosyaların yollarını, `folder`'a göre **göreli** ve `/`
ayıraçlı olarak, **sıralı** bir liste hâlinde döndürsün
(`os.path.relpath`, `.replace(os.sep, "/")`).
Örnek: `"data/old/sales-2025.csv"`.

**Beklenen çıktı:**

```
data/old/sales-2025.csv
data/sales.csv
data/stock.csv
```
