Klasörünün yanında hazır bir `project` klasörü var:

- `project/main.py`, `README.txt`, `LICENSE`
- `project/data/sales.csv`, `stock.csv`
- `project/data/old/sales-2025.csv`
- `project/src/app.py`, `utils.py`
- `project/notes/todo.txt`

`count_by_ext(folder)` fonksiyonunu yaz: `os.walk` ile klasörü alt
klasörleriyle dolaşsın ve her uzantıdan kaç dosya olduğunu sözlük olarak
döndürsün (`os.path.splitext`). Uzantısı olmayan dosyaların anahtarı `""`.

**Beklenen çıktı:**

```
'' 1
'.csv' 3
'.py' 3
'.txt' 2
```
