Write the function `split_path(path)`: split a file path into the tuple
`(folder, name, extension)`. `os.path.split` gives the folder and the file
name, `os.path.splitext` the name and the extension.
Example: `"data/raw/sales.csv"` → `("data/raw", "sales", ".csv")`.

**Expected output:**

```
('data/raw', 'sales', '.csv')
('', 'archive.tar', '.gz')
```
