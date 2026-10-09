Next to your file there is a ready `project` folder:

- `project/main.py`, `README.txt`, `LICENSE`
- `project/data/sales.csv`, `stock.csv`
- `project/data/old/sales-2025.csv`
- `project/src/app.py`, `utils.py`
- `project/notes/todo.txt`

Write the function `find_files(folder, ext)`: return the paths of the files
with extension `ext` in the folder and its subfolders, **relative** to
`folder` and with `/` separators, as a **sorted** list (`os.path.relpath`,
`.replace(os.sep, "/")`).
Example: `"data/old/sales-2025.csv"`.

**Expected output:**

```
data/old/sales-2025.csv
data/sales.csv
data/stock.csv
```
