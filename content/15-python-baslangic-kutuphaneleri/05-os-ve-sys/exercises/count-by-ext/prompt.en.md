Next to your file there is a ready `project` folder:

- `project/main.py`, `README.txt`, `LICENSE`
- `project/data/sales.csv`, `stock.csv`
- `project/data/old/sales-2025.csv`
- `project/src/app.py`, `utils.py`
- `project/notes/todo.txt`

Write the function `count_by_ext(folder)`: walk the folder with its
subfolders using `os.walk` and return how many files there are of each
extension as a dictionary (`os.path.splitext`). Files with no extension use
the key `""`.

**Expected output:**

```
'' 1
'.csv' 3
'.py' 3
'.txt' 2
```
