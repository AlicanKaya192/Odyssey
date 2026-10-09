There is a `logs` folder next to your file: `2025-11.txt`, `2025-12.txt`,
`2026-01.txt`, `2026-02.txt`, `README.txt`.

Write the function `archive_year(folder, year)`: move the `.txt` files in the
folder whose names start with `{year}-` into the folder
`folder/archive/{year}/` (`glob`, `shutil.move`) and return the file names in
that archive folder as a sorted list. Called a second time it must give the
same list without moving anything.

**Expected output:**

```
['2025-11.txt', '2025-12.txt']
['2026-01.txt', '2026-02.txt', 'README.txt']
```
