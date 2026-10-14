`grades.py` turns a score into a letter grade: 90 and above `A`, 80 and above `B`, 70 and above `C`, below that `F`.

Write **one** test in `main.py` that uses `@pytest.mark.parametrize`. It needs at least **five** rows, and they should try the edges:

- `90` → `A`, `89` → `B`
- `80` → `B`, `79` → `C`
- `70` → `C`, `69` → `F`

Each row counts as a separate test.
