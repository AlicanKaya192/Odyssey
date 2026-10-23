Data often needs cleaning. In `before.csv`, in the exercise's folder, each student's name sits in one column as `Last, First` (`"Abbott, Hannah"`), next to their `house`.

Implement a program that takes **two** command-line arguments: the name of an existing CSV file to read (columns `name`, `house`) and the name of a new CSV to write. It should split each name into a first and a last name and write the new file with the columns `first`, `last`, `house` (in that order, with a header row). Assume every student has both a first and a last name.

If there are not exactly two arguments (`Too few command-line arguments` / `Too many command-line arguments`) or the first file cannot be read (`Could not read invalid_file.csv`, with the file's name), exit via `sys.exit`. (In CS50 the file is `scourgify.py`.)

Hint: `csv.DictReader` and `csv.DictWriter`; `writer.writeheader()` writes the header. Open the file you write with `newline=""` so no blank lines appear on Windows.

## How to test

The cases CS50 gives; Odyssey runs each one in a separate folder and compares your output and the file you write.

- No input → output (nothing) (exit code 1)
- Command `python cozum.py 1.csv 2.csv 3.csv` → output (nothing) (exit code 1)
- Command `python cozum.py invalid_file.csv output.csv` → output (nothing) (exit code 1)
- Command `python cozum.py before.csv after.csv` → file written `after.csv`
- Command `python cozum.py class.csv clean.csv` → file written `clean.csv`
